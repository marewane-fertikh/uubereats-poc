# redis_poc/acteurs/client.py

import json
import uuid

from redis_poc.db import (
    initialiser_commande,
    lire_commande,
    publier_event,
    get_redis_connection,
)
from redis_poc.data_loader import get_random_restaurant, get_random_menu_for_restaurant

CLIENT_ID = "CLIENT_1"

CHANNEL_COMMANDE_LIVREE_CLIENT = "commande_livree_client"
CHANNEL_COMMANDE_CREEE = "commande_creee"


def main():
    print("=== CLIENT (Redis / PubSub) ===")
    print("Ce script simule un client qui passe une commande UberEats.\n")

    input("[CLIENT] Appuie sur Entrée pour créer une commande...\n")

    # 1) Choix d'un restaurant + menu réels à partir des JSON
    resto = get_random_restaurant()
    menu = get_random_menu_for_restaurant(resto["restaurant_id"])

    # 2) Génération d'un ID de commande unique
    commande_id = uuid.uuid4().hex[:8].upper()

    print("[CLIENT] Restaurant choisi :")
    print(f"  - {resto['restaurant_name']} (id={resto['restaurant_id']})")
    print("[CLIENT] Plat choisi :")
    print(f"  - {menu['menu_name']} (id={menu['menu_id']})\n")

    # 3) Création de la commande dans Redis
    initialiser_commande(commande_id, CLIENT_ID, resto, menu)
    print(f"[CLIENT] Commande {commande_id} créée dans Redis.")
    print("[CLIENT] État en base :")
    print(lire_commande(commande_id))
    print()

    # 4) Publication de l'évènement 'commande_creee'
    payload = {
        "commande_id": commande_id,
        "client_id": CLIENT_ID,
        "restaurant_id": resto["restaurant_id"],
        "restaurant_name": resto["restaurant_name"],
        "menu_id": menu["menu_id"],
        "menu_name": menu["menu_name"],
    }
    publier_event(CHANNEL_COMMANDE_CREEE, payload)
    print(f"[CLIENT] Évènement '{CHANNEL_COMMANDE_CREEE}' publié.\n")

    # 5) On s'abonne à 'commande_livree_client' pour être notifié
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
        cid = data.get("commande_id")
        if cid != commande_id:
            continue

        print(f"[CLIENT] ✅ Commande {commande_id} livrée !")
        print("[CLIENT] État final en base :")
        print(lire_commande(commande_id))
        break

    print("\n[CLIENT] Fin du client.")


if __name__ == "__main__":
    main()
