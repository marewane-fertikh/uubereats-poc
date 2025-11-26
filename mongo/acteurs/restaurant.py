# mongo/acteurs/restaurant.py
import time
import random
from redis_poc.logger import log_restaurant
from mongo.db import get_db


def main():
    print("=== RESTAURANT (MongoDB / Change Streams) ===")
    db = get_db()
    commandes = db["commandes"]

    log_restaurant("En attente de commandes à préparer...")

    with commandes.watch(full_document="updateLookup") as stream:
        for change in stream:
            doc = change["fullDocument"]
            if doc.get("statut") != "a_preparer":
                continue

            commande_id = doc["_id"]
            log_restaurant(f"Nouvelle commande à préparer : {commande_id}")
            print(f"[RESTAURANT] Détails : {doc['restaurant_name']} - {doc['menu_name']}")

            delai = random.uniform(8.0, 12.0)
            log_restaurant(f"Préparation en cours (~{delai:.1f}s)...")
            time.sleep(delai)

            commandes.update_one(
                {"_id": commande_id},
                {"$set": {"statut": "prete"}}
            )
            log_restaurant(f"Commande prête : {commande_id}")


if __name__ == "__main__":
    main()
