## backend/cli/demo.py

import json
from pathlib import Path

from optimizer.model import MenuItem
from optimizer.optimizer import Optimizer

seed_path = Path(__file__).resolve().parent.parent.parent / "seed" / "menu.json"
if not seed_path.exists():
    raise FileNotFoundError(seed_path)

data = json.loads(seed_path.read_text())
base_items = [MenuItem(**b) for b in data["bases"]]
target = MenuItem(**data["specialty"])
opt = Optimizer(base_items, data["addon_costs"], data["special_requests"])
print(opt.hack(target))
