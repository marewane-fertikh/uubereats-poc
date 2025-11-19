# mongo/acteurs/livreur.py

import random
import time

from mongo.db import ecouter_evenements, mettre_a_jour_statut
from mongo.models import STATUT_ASSIGNEE, STATUT_LIVREE


def main():
    print("=== LIVREUR (MongoDB / Change Streams) ===")

    # Le livreur attend toutes les commandes qui passent à 'assignee'
    for event in ecouter_evenements(STATUT_ASSIGNEE):
        commande_id = str(event["_id"])
        livreur_id = event.get("livreur_id")

        print(f"[LIVREUR] Nouvelle commande assignée : {commande_id}")
        print(f"[LIVREUR] Je suis le livreur : {livreur_id}")

        # Simulation du trajet
        temps = random.uniform(0.5, 2.0)
        print(f"[LIVREUR] Livraison en cours... (~{temps:.1f}s)")
        time.sleep(temps)

        mettre_a_jour_statut(commande_id, STATUT_LIVREE)
        print(f"[LIVREUR] → Commande livrée (statut = {STATUT_LIVREE}).\n")


if __name__ == "__main__":
    main()
