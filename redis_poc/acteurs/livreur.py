# redis/acteurs/livreur.py
import json
from redis_poc.db import get_redis_connection, lire_commande, publier_event, mettre_a_jour_statut

CHANNEL_COMMANDE_ASSIGNEE = "commande_assignee"
CHANNEL_COMMANDE_LIVREE = "commande_livree"


def main():
    print("=== LIVREUR ===")
    print("Ce script simule le livreur.")
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
        print(f"[LIVREUR] ID livreur : {livreur_id}")
        print("[LIVREUR] État actuel en base :")
        print(lire_commande(commande_id))

        input("[LIVREUR] Appuie sur Entrée après avoir livré la commande...\n")

        # Mettre à jour localement (optionnel mais logique)
        mettre_a_jour_statut(commande_id, "livree_par_livreur", livreur_id)

        # Signaler à la plateforme que la commande est livrée
        payload = {"commande_id": commande_id}
        publier_event(CHANNEL_COMMANDE_LIVREE, payload)
        print(
            f"[LIVREUR] Évènement '{CHANNEL_COMMANDE_LIVREE}' publié "
            f"pour {commande_id}\n"
        )


if __name__ == "__main__":
    main()
