# redis/acteurs/plateforme.py
import json
from redis_poc.db import (
    mettre_a_jour_statut,
    lire_commande,
    publier_event,
    get_redis_connection,
)

CHANNEL_COMMANDE_CREEE = "commande_creee"
CHANNEL_COMMANDE_A_PREPARER = "commande_a_preparer"
CHANNEL_COMMANDE_PRETE = "commande_prete"
CHANNEL_COMMANDE_ASSIGNEE = "commande_assignee"
CHANNEL_COMMANDE_LIVREE = "commande_livree"
CHANNEL_COMMANDE_LIVREE_CLIENT = "commande_livree_client"

LIVREUR_ID = "LIVREUR_1"


def main():
    print("=== PLATEFORME ===")
    print("Ce script simule la plateforme (UberEats).")
    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe(
        CHANNEL_COMMANDE_CREEE,
        CHANNEL_COMMANDE_PRETE,
        CHANNEL_COMMANDE_LIVREE,
    )

    print(
        f"[PLATEFORME] Abonné aux channels : "
        f"{CHANNEL_COMMANDE_CREEE}, {CHANNEL_COMMANDE_PRETE}, {CHANNEL_COMMANDE_LIVREE}\n"
    )

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        channel = message["channel"]
        data = json.loads(message["data"])
        commande_id = data.get("commande_id")

        if channel == CHANNEL_COMMANDE_CREEE:
            # 1) La commande arrive depuis le client
            print(f"[PLATEFORME] Reçu '{CHANNEL_COMMANDE_CREEE}' pour {commande_id}")
            mettre_a_jour_statut(commande_id, "reçue_par_plateforme")
            print("[PLATEFORME] Commande après mise à jour :")
            print(lire_commande(commande_id))

            # 2) On envoie la commande au restaurant
            payload = {"commande_id": commande_id}
            publier_event(CHANNEL_COMMANDE_A_PREPARER, payload)
            print(
                f"[PLATEFORME] Évènement '{CHANNEL_COMMANDE_A_PREPARER}' publié "
                f"pour {commande_id}\n"
            )

        elif channel == CHANNEL_COMMANDE_PRETE:
            # 3) Le restaurant signale que la commande est prête
            print(f"[PLATEFORME] Reçu '{CHANNEL_COMMANDE_PRETE}' pour {commande_id}")
            mettre_a_jour_statut(commande_id, "prete")
            print("[PLATEFORME] Commande après mise à jour :")
            print(lire_commande(commande_id))

            # 4) On assigne un livreur
            mettre_a_jour_statut(commande_id, "assignée", LIVREUR_ID)
            payload = {"commande_id": commande_id, "livreur_id": LIVREUR_ID}
            publier_event(CHANNEL_COMMANDE_ASSIGNEE, payload)
            print(
                f"[PLATEFORME] Évènement '{CHANNEL_COMMANDE_ASSIGNEE}' publié "
                f"pour {commande_id} avec livreur {LIVREUR_ID}\n"
            )

        elif channel == CHANNEL_COMMANDE_LIVREE:
            # 5) Le livreur signale que la commande est livrée
            print(f"[PLATEFORME] Reçu '{CHANNEL_COMMANDE_LIVREE}' pour {commande_id}")
            mettre_a_jour_statut(commande_id, "livree")
            print("[PLATEFORME] Commande après mise à jour :")
            print(lire_commande(commande_id))

            # 6) On notifie le client
            payload = {"commande_id": commande_id}
            publier_event(CHANNEL_COMMANDE_LIVREE_CLIENT, payload)
            print(
                f"[PLATEFORME] Évènement '{CHANNEL_COMMANDE_LIVREE_CLIENT}' "
                f"publié pour {commande_id}\n"
            )


if __name__ == "__main__":
    main()
