# redis_poc/acteurs/livreur.py

import json
import time

from redis_poc.db import (
    get_redis_connection,
    lire_commande,
    publier_event,
    mettre_a_jour_statut,
)

CHANNEL_COMMANDE_ASSIGNEE = "commande_assignee"
CHANNEL_COMMANDE_LIVREE = "commande_livree"


def main():
    print("=== LIVREUR (Redis / PubSub) ===")
    print("Ce script simule le livreur.\n")
    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_COMMANDE_ASSIGNEE)

    print(f"[LIVREUR] Abonné au channel '{CHANNEL_COMMANDE_ASSIGNEE}'\n")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])
        commande_id = data.get("commande_id")
        livreur_id = data.get("livreur_id")

        print(f"[LIVREUR] Nouvelle commande assignée : {commande_id}")
        print(f"[LIVREUR] Je suis le livreur : {livreur_id}")
        print("[LIVREUR] État actuel en base :")
        print(lire_commande(commande_id))

        print("[LIVREUR] Livraison en cours (~1.5s)...")
        time.sleep(1.5)

        # Mettre à jour le statut
        mettre_a_jour_statut(commande_id, "livree_par_livreur", livreur_id)

        # Signaler à la plateforme que la commande est livrée
        payload = {"commande_id": commande_id}
        publier_event(CHANNEL_COMMANDE_LIVREE, payload)
        print(
            f"[LIVREUR] → Évènement '{CHANNEL_COMMANDE_LIVREE}' publié "
            f"pour {commande_id}\n"
        )


if __name__ == "__main__":
    main()
