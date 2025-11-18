# redis/acteurs/client.py
import json
from redis_poc.db import (
    initialiser_commande,
    lire_commande,
    publier_event,
    get_redis_connection,
)

COMMANDE_ID = "CMD123"
CLIENT_ID = "CLIENT_1"
RESTAURANT_ID = "RESTO_1"

CHANNEL_COMMANDE_LIVREE_CLIENT = "commande_livree_client"
CHANNEL_COMMANDE_CREEE = "commande_creee"


def main():
    print("=== CLIENT ===")
    print("Ce script simule un client qui passe une commande UberEats.")
    input("Appuie sur Entrée pour créer une commande...\n")

    # 1) Création de la commande dans Redis
    initialiser_commande(COMMANDE_ID, CLIENT_ID, RESTAURANT_ID)
    print(f"[CLIENT] Commande {COMMANDE_ID} créée dans Redis.")

    # 2) Publication de l'évènement 'commande_creee'
    payload = {
        "commande_id": COMMANDE_ID,
        "client_id": CLIENT_ID,
        "restaurant_id": RESTAURANT_ID,
    }
    publier_event(CHANNEL_COMMANDE_CREEE, payload)
    print(f"[CLIENT] Évènement '{CHANNEL_COMMANDE_CREEE}' publié : {payload}")
    print()

    # 3) On s'abonne à 'commande_livree_client' pour être notifié
    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_COMMANDE_LIVREE_CLIENT)

    print(
        f"[CLIENT] En attente de la notification finale sur le channel "
        f"'{CHANNEL_COMMANDE_LIVREE_CLIENT}'...\n"
    )

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])
        commande_id = data.get("commande_id")
        if commande_id != COMMANDE_ID:
            # dans ce POC on a une seule commande, mais on filtre quand même
            continue

        print(f"[CLIENT] ✅ Commande {commande_id} livrée !")
        print("[CLIENT] État final en base :")
        print(lire_commande(COMMANDE_ID))
        break

    print("\n[CLIENT] Fin du client.")


if __name__ == "__main__":
    main()
