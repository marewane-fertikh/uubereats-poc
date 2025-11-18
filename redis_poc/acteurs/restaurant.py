# redis/acteurs/restaurant.py
import json
from redis_poc.db import get_redis_connection, lire_commande, publier_event, mettre_a_jour_statut

CHANNEL_COMMANDE_A_PREPARER = "commande_a_preparer"
CHANNEL_COMMANDE_PRETE = "commande_prete"


def main():
    print("=== RESTAURANT ===")
    print("Ce script simule le restaurant.")
    r = get_redis_connection()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_COMMANDE_A_PREPARER)

    print(f"[RESTAURANT] Abonné au channel '{CHANNEL_COMMANDE_A_PREPARER}'\n")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])
        commande_id = data.get("commande_id")
        print(f"[RESTAURANT] Nouvelle commande à préparer : {commande_id}")
        print("[RESTAURANT] État actuel en base :")
        print(lire_commande(commande_id))

        input("[RESTAURANT] Appuie sur Entrée quand la commande est prête...\n")

        # Met à jour le statut localement (optionnel mais cohérent)
        mettre_a_jour_statut(commande_id, "prete_par_restaurant")

        # Signale à la plateforme que la commande est prête
        payload = {"commande_id": commande_id}
        publier_event(CHANNEL_COMMANDE_PRETE, payload)
        print(
            f"[RESTAURANT] Évènement '{CHANNEL_COMMANDE_PRETE}' publié "
            f"pour {commande_id}\n"
        )


if __name__ == "__main__":
    main()
