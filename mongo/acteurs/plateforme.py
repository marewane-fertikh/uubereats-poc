# mongo/acteurs/plateforme.py
import time
from redis_poc.logger import log_plateforme
from mongo.db import get_db


LIVREURS = ["LIVREUR_1"]  # version simple (1 livreur fixe ici)


def handle_cree(commandes, doc):
    commande_id = doc["_id"]
    log_plateforme(f"Commande créée : {commande_id}")
    log_plateforme("→ commande envoyée au restaurant (statut = 'a_preparer')")
    commandes.update_one(
        {"_id": commande_id},
        {"$set": {"statut": "a_preparer"}}
    )


def handle_prete(commandes, doc):
    commande_id = doc["_id"]
    log_plateforme(f"Commande prête : {commande_id}")

    livreur_id = LIVREURS[0]  # version simple
    log_plateforme(f"Livreur assigné : {livreur_id}")

    commandes.update_one(
        {"_id": commande_id},
        {"$set": {"statut": "assignee", "livreur_id": livreur_id}}
    )


def handle_livree(commandes, doc):
    commande_id = doc["_id"]
    log_plateforme(f"Commande livrée : {commande_id}")
    log_plateforme("→ Notification client (statut = 'notification_client')")

    commandes.update_one(
        {"_id": commande_id},
        {"$set": {"statut": "notification_client"}}
    )


def main():
    print("=== PLATEFORME (MongoDB / Change Streams) ===")
    db = get_db()
    commandes = db["commandes"]

    log_plateforme("En attente d'événements...")

    with commandes.watch(full_document="updateLookup") as stream:
        for change in stream:
            doc = change["fullDocument"]
            statut = doc.get("statut")
            commande_id = doc["_id"]

            if statut == "cree":
                handle_cree(commandes, doc)
            elif statut == "prete":
                handle_prete(commandes, doc)
            elif statut == "livree":
                handle_livree(commandes, doc)


if __name__ == "__main__":
    main()
