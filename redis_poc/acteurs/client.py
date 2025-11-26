import json
import random
import time
from redis_poc.db import get_redis_connection, save_commande, read_commande
from redis_poc.data_loader import get_random_restaurant_and_menu
from redis_poc.logger import log_client

def main():
    log_client("=== CLIENT (Redis) ===")
    input("Appuie sur Entrée pour passer une commande...")

    r = get_redis_connection()

    resto, menu, client_id = get_random_restaurant_and_menu()

    commande_id = hex(random.getrandbits(48))[2:].upper()

    commande = {
        "commande_id": commande_id,
        "client_id": client_id,
        "restaurant_id": resto["id"],
        "restaurant_name": resto["name"],
        "menu_id": menu["menu_id"],
        "menu_name": menu["name"],
        "livreur_id": "",
        "statut": "cree"
    }

    save_commande(r, commande_id, commande)

    log_client("Commande créée : " + commande_id)
    print(json.dumps(commande, indent=4))

    r.publish("commande_creee", json.dumps({"commande_id": commande_id}))
    log_client("→ commande_creee publiée")

    # Écoute la livraison finale
    pubsub = r.pubsub()
    pubsub.subscribe("commande_livree_client")

    log_client(f"En attente de la livraison de {commande_id}…")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        data = json.loads(msg["data"])
        if data["commande_id"] == commande_id:
            log_client(f"✔️ Commande {commande_id} livrée !")
            final_state = read_commande(r, commande_id)
            print("[CLIENT] État final :")
            print(json.dumps(final_state, indent=4))
            break

if __name__ == "__main__":
    main()
