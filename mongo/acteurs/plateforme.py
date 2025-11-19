# mongo/acteurs/plateforme.py

import time

from mongo.db import ecouter_evenements, mettre_a_jour_statut
from mongo.models import (
    STATUT_CREE,
    STATUT_A_PREPARER,
    STATUT_PRETE,
    STATUT_ASSIGNEE,
    STATUT_LIVREE,
    STATUT_NOTIFIE_CLIENT,
)

"""
Rôle de la plateforme (orchestrateur) :

1. Écouter les commandes créées (statut = 'cree')
2. Envoyer au restaurant   → statut = 'a_preparer'
3. Attendre que le restaurant termine → statut = 'prete'
4. Assigner un livreur     → statut = 'assignee'
5. Attendre la livraison   → statut = 'livree'
6. Notifier le client      → statut = 'notification_client'
"""

LIVREUR_FIXE = "LIVREUR_1"


def main():
    print("=== PLATEFORME (MongoDB / Change Streams) ===")
    print("En attente de nouvelles commandes...\n")

    # 1) écouter toutes les commandes qui passent à 'cree'
    for event in ecouter_evenements(STATUT_CREE):
        commande_id = str(event["_id"])
        print(f"[PLATEFORME] Nouvelle commande détectée : {commande_id}")

        # 2) transmettre au restaurant
        mettre_a_jour_statut(commande_id, STATUT_A_PREPARER)
        print(f"[PLATEFORME] → Commande envoyée au restaurant (statut = {STATUT_A_PREPARER})")

        # 3) attendre que le restaurant marque la commande comme 'prete'
        for ev_prete in ecouter_evenements(STATUT_PRETE, commande_id):
            print(f"[PLATEFORME] Commande prête : {commande_id}")
            time.sleep(0.3)

            # 4) assigner un livreur
            mettre_a_jour_statut(commande_id, STATUT_ASSIGNEE, LIVREUR_FIXE)
            print(f"[PLATEFORME] → Livreur assigné : {LIVREUR_FIXE} (statut = {STATUT_ASSIGNEE})")
            break

        # 5) attendre que le livreur marque la commande comme 'livree'
        for ev_livree in ecouter_evenements(STATUT_LIVREE, commande_id):
            print(f"[PLATEFORME] Commande livrée par le livreur : {commande_id}")
            time.sleep(0.3)

            # 6) notifier le client
            mettre_a_jour_statut(commande_id, STATUT_NOTIFIE_CLIENT)
            print(f"[PLATEFORME] → Notification envoyée au client (statut = {STATUT_NOTIFIE_CLIENT}).\n")
            break


if __name__ == "__main__":
    main()
