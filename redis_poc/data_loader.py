# redis_poc/data_loader.py
"""
Chargement des données depuis data/restaurants.json et data/menus.json.

On ne dépend pas d'un schéma exact : on essaie de récupérer des champs
logiques (id, name, restaurant_id, etc.) et on reste robuste.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

RESTAURANTS_JSON = DATA_DIR / "restaurants.json"
MENUS_JSON = DATA_DIR / "menus.json"


def _load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} doit contenir une liste de documents JSON")
    return data


def _extract_restaurant_id(resto: Dict[str, Any], default: str) -> str:
    return str(
        resto.get("id")
        or resto.get("restaurant_id")
        or resto.get("Restaurant ID")
        or resto.get("restaurantId")
        or resto.get("id_restaurant")
        or default
    )


def _extract_restaurant_name(resto: Dict[str, Any]) -> str:
    return str(
        resto.get("name")
        or resto.get("restaurant_name")
        or resto.get("Restaurant Name")
        or resto.get("Nom")
        or "Restaurant inconnu"
    )


def _extract_menu_id(menu: Dict[str, Any], default: str) -> str:
    return str(
        menu.get("id")
        or menu.get("menu_id")
        or menu.get("Item ID")
        or menu.get("id_menu")
        or default
    )


def _extract_menu_name(menu: Dict[str, Any]) -> str:
    return str(
        menu.get("name")
        or menu.get("item_name")
        or menu.get("Menu Item")
        or menu.get("Nom")
        or "Plat inconnu"
    )


def load_restaurants() -> list[dict]:
    return _load_json(RESTAURANTS_JSON)


def load_menus() -> list[dict]:
    return _load_json(MENUS_JSON)


def get_random_restaurant() -> dict:
    """
    Renvoie un dict normalisé :
    {
        "restaurant_id": "...",
        "restaurant_name": "..."
        "raw": {...}  # doc complet d'origine
    }
    """
    restaurants = load_restaurants()
    if not restaurants:
        raise RuntimeError("Aucun restaurant dans restaurants.json")

    raw = random.choice(restaurants)
    idx = restaurants.index(raw)
    restaurant_id = _extract_restaurant_id(raw, default=str(idx))
    restaurant_name = _extract_restaurant_name(raw)

    return {
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant_name,
        "raw": raw,
    }


def get_random_menu_for_restaurant(restaurant_id: str) -> dict:
    """
    Renvoie un dict normalisé :
    {
        "menu_id": "...",
        "menu_name": "...",
        "raw": {...}
    }

    On essaie de filtrer par restaurant_id si possible, sinon on prend un menu au hasard.
    """
    menus = load_menus()
    if not menus:
        raise RuntimeError("Aucun menu dans menus.json")

    # On cherche les menus qui semblent liés à ce restaurant
    candidates: list[dict] = []
    for m in menus:
        rid = str(
            m.get("restaurant_id")
            or m.get("Restaurant ID")
            or m.get("restaurantId")
            or m.get("id_restaurant")
            or ""
        )
        if rid == str(restaurant_id):
            candidates.append(m)

    if candidates:
        raw = random.choice(candidates)
    else:
        # fallback : n'importe quel menu
        raw = random.choice(menus)

    midx = menus.index(raw)
    menu_id = _extract_menu_id(raw, default=str(midx))
    menu_name = _extract_menu_name(raw)

    return {
        "menu_id": menu_id,
        "menu_name": menu_name,
        "raw": raw,
    }
