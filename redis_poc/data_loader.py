import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RESTAURANTS_JSON = BASE / "data" / "restaurants.json"
MENUS_JSON = BASE / "data" / "menus.json"

# Charger JSON (peu importe si data_local/data differents, tu as déjà le lien symbolique)
def _load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def load_restaurants():
    return _load_json(RESTAURANTS_JSON)

def load_menus():
    menus = _load_json(MENUS_JSON)

    # Ajouter un menu_id artificiel si absent
    for idx, m in enumerate(menus):
        if "menu_id" not in m:
            m["menu_id"] = idx + 1   # simple identifiant numérique

    return menus

def get_random_restaurant_and_menu():
    restaurants = load_restaurants()
    menus = load_menus()

    resto = random.choice(restaurants)

    # Menus correspondant à ce restaurant
    menus_for_resto = [
        m for m in menus if str(m["restaurant_id"]) == str(resto["id"])
    ]

    if not menus_for_resto:
        raise ValueError(f"Aucun menu pour restaurant {resto['id']}")

    menu = random.choice(menus_for_resto)

    # Génération d’un client_id simple
    client_id = f"CLIENT_{random.randint(1000, 9999)}"

    return resto, menu, client_id
