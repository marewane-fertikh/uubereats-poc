import json
import time
import random
from redis_poc.db import get_redis_connection, read_commande, save_commande
from redis_poc.logger import log_restaurant

def main():
    log_restaurant("=== RESTAURANT (Redis) ===")

    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe("commande_a_preparer")

    log_restaurant("Abonné à 'commande_a_preparer'")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        data = json.loads(msg["data"])
        cmd_id = data["commande_id"]

        log_restaurant(f"Nouvelle commande à préparer : {cmd_id}")

        preparation_time = random.uniform(2.0, 5.0)  # réaliste mais pas trop long
        print(f"[RESTAURANT] ⏳ Préparation (~{preparation_time:.1f}s)…")
        time.sleep(preparation_time)

        commande = read_commande(r, cmd_id)
        commande["statut"] = "prete"
        save_commande(r, cmd_id, commande)

        r.publish("commande_prete", json.dumps({"commande_id": cmd_id}))
        log_restaurant("→ commande_prete publiée")

if __name__ == "__main__":
    main()
