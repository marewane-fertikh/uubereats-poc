# mongo/acteurs/restaurant.py

import random
import time

from mongo.db import ecouter_evenements, mettre_a_jour_statut
from mongo.models import STATUT_A_PREPARER, STATUT_PRETE


def main():
    print("=== RESTAURANT (MongoDB / Change Streams) ===")

    # Le restaurant prépare toutes les commandes qui passent à 'a_preparer'
    for event in ecouter_evenements(STATUT_A_PREPARER):
        commande_id = str(event["_id"])
        print(f"[RESTAURANT] Nouvelle commande à préparer : {commande_id}")

        # Simulation du temps de préparation
        temps = random.uniform(0.5, 2.0)
        print(f"[RESTAURANT] Préparation en cours... (~{temps:.1f}s)")
        time.sleep(temps)

        mettre_a_jour_statut(commande_id, STATUT_PRETE)
        print(f"[RESTAURANT] → Commande prête (statut = {STATUT_PRETE}).\n")


if __name__ == "__main__":
    main()
