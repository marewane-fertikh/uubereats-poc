# mongo/acteurs/client.py
import time
import random
import json
from bson import ObjectId

from redis_poc.logger import log_client
from mongo.db import get_db


def pick_random_restaurant_and_menu(db):
    restaurants = db["restaurants"]
    menus = db["menus"]

    # 1) Restaurant aléatoire
    resto = next(restaurants.aggregate([{"$sample": {"size": 1}}]))
    resto_id = str(resto["id"])

    # 2) Plat aléatoire de ce restaurant
    menu = next(
        menus.aggregate([
            {"$match": {"restaurant_id": resto_id}},
            {"$sample": {"size": 1}}
        ])
    )

    return resto, menu


def main():
    print("=== CLIENT (MongoDB / Change Streams) ===")

    db = get_db()
    commandes = db["commandes"]

    input("Appuie sur Entrée pour passer une commande...")

    # Tirage aléatoire restaurant + plat 
    resto, menu = pick_random_restaurant_and_menu(db)
    client_id = f"CLIENT_{random.randint(1000, 9999)}"

    print(f"[CLIENT] Restaurant choisi : {resto['name']} (id={resto['id']})")
    print(f"[CLIENT] Plat choisi      : {menu['name']} (id={menu.get('id', menu.get('_id'))})")

    commande_doc = {
        "restaurant_id": str(resto["id"]),
        "menu_id": str(menu.get("id", menu.get("_id"))),
        "client_id": client_id,
        "livreur_id": None,
        "restaurant_name": resto["name"],
        "menu_name": menu["name"],
        "statut": "cree",
        "timestamp": time.time(),
    }

    # Création de la commande 
    result = commandes.insert_one(commande_doc)
    commande_id = result.inserted_id

    log_client(f"Commande créée : {commande_id}")
    print(json.dumps({**commande_doc, "_id": str(commande_id)}, indent=4, ensure_ascii=False))

    log_client("En attente de la notification finale (statut = notification_client)...")

    # Change Stream : on attend la notification finale 
    pipeline = [
        {"$match": {
            "operationType": "update",
            "documentKey._id": commande_id
        }}
    ]

    with commandes.watch(pipeline=pipeline, full_document="updateLookup") as stream:
        for change in stream:
            doc = change["fullDocument"]
            statut = doc.get("statut")

            if statut == "notification_client":
                log_client(f"✅ Commande {commande_id} livrée !")
                print("[CLIENT] État final :")
                final = {
                    "_id": str(doc["_id"]),
                    "client_id": doc["client_id"],
                    "restaurant_id": doc["restaurant_id"],
                    "restaurant_name": doc["restaurant_name"],
                    "menu_id": doc["menu_id"],
                    "menu_name": doc["menu_name"],
                    "livreur_id": doc.get("livreur_id"),
                    "statut": doc["statut"],
                }
                print(json.dumps(final, indent=4, ensure_ascii=False))
                break


if __name__ == "__main__":
    main()
