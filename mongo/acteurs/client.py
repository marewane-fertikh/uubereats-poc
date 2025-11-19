# mongo/acteurs/client.py

import random

from mongo.db import creer_commande, ecouter_evenements
from mongo.models import STATUT_NOTIFIE_CLIENT


def main():
    print("=== CLIENT (MongoDB / Change Streams) ===")

    # Pour le POC : on choisit un restaurant + menu au hasard
    restaurant_id = str(random.randint(1, 5000))
    menu_id = str(random.randint(1, 400000))
    client_id = "CLIENT_1"

    print("[CLIENT] Création de la commande...")
    commande_id = creer_commande(restaurant_id, menu_id, client_id)
    print(f"[CLIENT] Commande créée avec l'id : {commande_id}")
    print("[CLIENT] En attente de la notification de livraison...\n")

    # On attend le statut final "notification_client" pour cette commande
    for event in ecouter_evenements(STATUT_NOTIFIE_CLIENT, commande_id):
        print("🟢 [CLIENT] Commande livrée et notification reçue !")
        print(f"[CLIENT] Détails finaux : {event}")
        break


if __name__ == "__main__":
    main()
