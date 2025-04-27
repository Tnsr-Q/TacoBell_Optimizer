## tests/test_optimizer.py

import json
import importlib.resources as pkg_resources

from backend.optimizer import model, optimizer, data

# Use the same package-relative approach for tests
data_json = json.loads(pkg_resources.files(data).joinpath("menu.json").read_text())
base_items = [model.MenuItem(**b) for b in data_json["bases"]]
target = model.MenuItem(**data_json["specialty"])
opt = optimizer.Optimizer(base_items, data_json["addon_costs"], data_json["special_requests"])


def test_mexican_pizza_returns_original():
    res = opt.hack(target)
    assert res.message and "Order original" in res.message
