## backend/optimizer/store.py

"""Temporary seed‑backed store layer – toggled by USE_DB flag."""
import json
import pathlib

import backoff
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable  # Updated import path

from backend.app.core.config import settings
from .model import MenuItem

_seed_path = pathlib.Path(__file__).parent.parent.parent / "seed" / "menu.json"
_seed = json.loads(_seed_path.read_text())


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def get_session():
    return GraphDatabase.driver(settings.NEO4J_BOLT_URL).session()


def get_item(item_id: str):
    if settings.USE_DB:
        # TODO: real Neo4j query
        pass
    return MenuItem(**_seed["specialty"]) if item_id == "specialty" else None


def get_bases(zip: str | None = None):
    if settings.USE_DB:
        pass
    return [MenuItem(**b) for b in _seed["bases"]]


def get_addon_costs(zip: str | None = None):
    return _seed["addon_costs"]


def get_special_requests():
    return _seed["special_requests"]
