import json
import time
import random
from redis_poc.db import get_redis_connection, read_commande, save_commande
from redis_poc.logger import log_livreur

def compute_delivery_times():
    distance = random.uniform(0.5, 5.0)
    pickup = random.uniform(1.0, 2.0)
    travel = distance * random.uniform(0.8, 1.3)
    return pickup, travel, round(distance, 1)

def main():
    log_livreur("LIVREUR_1", "=== LIVREUR (Redis) ===")

    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe("commande_assignee")

    livreur_id = "LIVREUR_1"

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        data = json.loads(msg["data"])
        if data["livreur_id"] != livreur_id:
            continue

        cmd_id = data["commande_id"]
        log_livreur(livreur_id, "Nouvelle commande assignée")

        pickup, travel, dist = compute_delivery_times()

        log_livreur(livreur_id, f"Distance estimée : {dist} km")
        print(f"[LIVREUR] ⏳ Récupération (~{pickup:.1f}s)…")
        time.sleep(pickup)

        log_livreur(livreur_id, "🛣️ En route vers le client")
        time.sleep(travel)

        commande = read_commande(r, cmd_id)
        commande["statut"] = "livree"
        save_commande(r, cmd_id, commande)

        r.publish("commande_livree", json.dumps({"commande_id": cmd_id}))
        log_livreur(livreur_id, f"→ commande_livree publiée ({cmd_id})")

if __name__ == "__main__":
    main()
