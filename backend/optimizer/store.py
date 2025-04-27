## backend/optimizer/store.py

"""Temporary seed‑backed store layer – toggled by USE_DB flag."""
import json
import pathlib

import backoff
from neo4j import GraphDatabase
# Try to import ServiceUnavailable from different possible locations
try:
    from neo4j.exceptions import ServiceUnavailable
except ImportError:
    try:
        from neo4j import ServiceUnavailable
    except ImportError:
        # Define a fallback if we can't import it
        class ServiceUnavailable(Exception):
            """Fallback exception if neo4j.ServiceUnavailable is not available."""
            pass

from backend.app.core.config import settings
from .model import MenuItem

_seed_path = pathlib.Path(__file__).parent.parent.parent / "seed" / "menu.json"
_seed = json.loads(_seed_path.read_text())


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=5)
def get_session():
    """Get Neo4j session with retry logic."""
    return GraphDatabase.driver(settings.NEO4J_BOLT_URL).session()


def get_item(item_id: str) -> MenuItem:
    """Get menu item by ID."""
    if settings.USE_DB:
        # TODO: real Neo4j query
        pass
    return MenuItem(**_seed["specialty"]) if item_id == "specialty" else None


def get_bases(zip: str | None = None) -> list[MenuItem]:
    """Get base menu items, optionally filtered by zip code."""
    if settings.USE_DB:
        # TODO: real Neo4j query
        pass
    return [MenuItem(**b) for b in _seed["bases"]]


def get_addon_costs(zip: str | None = None) -> dict:
    """Get addon costs, optionally by location."""
    if settings.USE_DB:
        # TODO: real Neo4j query
        pass
    return _seed["addon_costs"]


def get_special_requests() -> dict:
    """Get special request configurations."""
    if settings.USE_DB:
        # TODO: real Neo4j query
        pass
    return _seed["special_requests"]
