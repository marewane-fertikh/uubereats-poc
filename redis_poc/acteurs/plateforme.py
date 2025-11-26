import json
from redis_poc.db import get_redis_connection, read_commande, save_commande
from redis_poc.logger import log_plateforme

def main():
    log_plateforme("=== PLATEFORME (Redis) ===")

    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe("commande_creee", "commande_prete", "commande_livree")

    log_plateforme("Abonné aux événements.")
    log_plateforme("En attente…")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        event = msg["channel"]
        data = json.loads(msg["data"])

        if event == "commande_creee":
            commande_id = data["commande_id"]
            log_plateforme("Commande reçue")
            r.publish("commande_a_preparer", json.dumps({"commande_id": commande_id}))
            log_plateforme("Commande envoyée au restaurant")

        elif event == "commande_prete":
            commande_id = data["commande_id"]
            log_plateforme("Commande reçue")

            # Affecte un livreur fixe
            livreur_id = "LIVREUR_1"

            cmd = read_commande(r, commande_id)
            cmd["livreur_id"] = livreur_id
            save_commande(r, commande_id, cmd)

            r.publish("commande_assignee", json.dumps({
                "commande_id": commande_id,
                "livreur_id": livreur_id
            }))

            log_plateforme("Livreur assigné")

        elif event == "commande_livree":
            commande_id = data["commande_id"]
            r.publish("commande_livree_client", json.dumps({"commande_id": commande_id}))

if __name__ == "__main__":
    main()
