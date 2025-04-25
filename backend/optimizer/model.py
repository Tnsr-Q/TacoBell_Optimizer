## backend/optimizer/model.py

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

class ItemType(str, Enum):
    TACO = "taco"
    BURRITO = "burrito"
    FLATBREAD = "flatbread"
    CHALUPA = "chalupa"
    QUESADILLA = "quesadilla"

@dataclass(frozen=True)
class MenuItem:
    id: str
    name: str
    price: float
    type: ItemType
    ingredients: List[str]

@dataclass
class HackResult:
    base_items: List[str]
    customizations: List[str]
    total_cost: float
    savings: float
    feasibility: float
    message: str | None = None
    metadata: Dict[str, str] = field(default_factory=dict)


