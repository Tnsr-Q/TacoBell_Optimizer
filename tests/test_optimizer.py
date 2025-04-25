## tests/test_optimizer.py

import json
import pathlib

from backend.optimizer import model, optimizer

data = json.loads(
    (pathlib.Path(__file__).parent.parent / "seed" / "menu.json").read_text()
)
base_items = [model.MenuItem(**b) for b in data["bases"]]
target = model.MenuItem(**data["specialty"])
opt = optimizer.Optimizer(base_items, data["addon_costs"], data["special_requests"])


def test_mexican_pizza_returns_original():
    res = opt.hack(target)
    assert res.message and "Order original" in res.message
