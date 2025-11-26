# mongo/acteurs/livreur.py
import time
import random
from redis_poc.logger import log_livreur
from mongo.db import get_db


def compute_delivery_times():
    """Compute pickup and travel times and a mock distance for demo purposes.

    Returns:
        tuple: (pickup_seconds: float, travel_seconds: float, distance_km: float)
    """
    distance_km = random.uniform(0.5, 8.0)
    pickup_time = random.uniform(1.0, 2.0)
    travel_time = distance_km * random.uniform(1.2, 1.6)
    return pickup_time, travel_time, round(distance_km, 1)


def main():
    print("=== LIVREUR (MongoDB / Change Streams) ===")
    db = get_db()
    commandes = db["commandes"]

    print("[LIVREUR] En attente de commandes assignées...")

    with commandes.watch(full_document="updateLookup") as stream:
        for change in stream:
            doc = change["fullDocument"]
            if doc.get("statut") != "assignee":
                continue

            commande_id = doc["_id"]
            livreur_id = doc.get("livreur_id", "LIVREUR_1")

            log_livreur(livreur_id, f"Nouvelle commande assignée : {commande_id}")
            pickup, travel, dist = compute_delivery_times()
            log_livreur(livreur_id, f"Distance estimée : {dist:.1f} km")

            log_livreur(livreur_id, f"⏳ Récupération (~{pickup:.1f}s)...")
            time.sleep(pickup)

            log_livreur(livreur_id, f"🛣️ En route (~{travel:.1f}s)...")
            time.sleep(travel)

            commandes.update_one(
                {"_id": commande_id},
                {"$set": {"statut": "livree"}}
            )
            log_livreur(livreur_id, f"→ commande_livree publiée ({commande_id})")


if __name__ == "__main__":
    main()
