## backend/optimizer/optimizer.py

from typing import Dict, List

from ortools.sat.python import cp_model

from .model import HackResult, MenuItem


class Optimizer:
    """MILP / CP‑SAT cost minimizer.
    k_max – max number of base items (default 2).
    """

    def __init__(
        self,
        base_items: List[MenuItem],
        addon_costs: Dict[str, float],
        special_requests: Dict[str, dict],
        k_max: int = 2,
    ):
        self.base_items = base_items
        self.addon_costs = addon_costs
        self.special_requests = special_requests
        self.k_max = k_max

    def hack(self, target: MenuItem) -> HackResult:
        mdl = cp_model.CpModel()
        B = range(len(self.base_items))
        y = {b: mdl.NewBoolVar(f"y_{b}") for b in B}  # base chosen

        # Must choose at least one base (no‑null solution)
        mdl.Add(sum(y.values()) >= 1)
        mdl.Add(sum(y.values()) <= self.k_max)

        # lock type mismatch
        for b, item in enumerate(self.base_items):
            if item.type != target.type:
                mdl.Add(y[b] == 0)

        # ingredient coverage vars
        ing_needed = set(target.ingredients)
        x = {(i, b): mdl.NewBoolVar(f"x_{i}_{b}") for i in ing_needed for b in B}

        for i in ing_needed:
            mdl.Add(sum(x[i, b] for b in B) >= 1)
            for b in B:
                if i not in self.base_items[b].ingredients:
                    mdl.Add(x[i, b] <= y[b])
                else:
                    mdl.Add(x[i, b] == 0)  # already present → no add‑on needed

        # cost objective
        cost_expr = sum(self.base_items[b].price * y[b] for b in B)
        for i in ing_needed:
            for b in B:
                if i not in self.base_items[b].ingredients:
                    cost_expr += self.addon_costs.get(i, 999) * x[i, b]

        # tie‑breaker – fewer bases favoured
        cost_expr += 0.001 * sum(y[b] for b in B)
        mdl.Minimize(cost_expr)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 0.20
        status = solver.Solve(mdl)

        if status != cp_model.OPTIMAL:
            return HackResult(
                [], [], target.price, 0, 1, message=f"Order original {target.name}"
            )

        total = solver.ObjectiveValue()
        savings = target.price - total
        if savings <= 0.01:
            return HackResult(
                [], [], target.price, 0, 1, message=f"Order original {target.name}"
            )

        bases = [self.base_items[b].name for b in B if solver.Value(y[b])]
        # TODO: build customizations list properly
        return HackResult(bases, [], total, savings, 1.0)
