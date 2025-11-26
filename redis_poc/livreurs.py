# redis_poc/livreurs.py
"""
Gestion des livreurs côté Redis.

Idée :
- On garde une liste de prénoms "simples".
- À chaque lancement d'un process livreur, on incrémente un compteur Redis.
- On choisit le prénom en fonction du numéro (modulo la taille de la liste).
"""

from __future__ import annotations

from typing import Tuple

from redis_poc.db import get_redis_connection

LIVREUR_NAMES = ["Adam", "Nina", "Yassine", "Lina", "Lucas"]


def reserver_livreur() -> Tuple[str, str]:
    """
    Réserve un identifiant de livreur unique.

    Retourne (livreur_id, nom_affiche).
    Exemple : ("LIVREUR_1", "Livreur Adam (#1)")
    """
    r = get_redis_connection()
    num = r.incr("livreurs:counter")  # 1, 2, 3, ...

    index = (num - 1) % len(LIVREUR_NAMES)
    prenom = LIVREUR_NAMES[index]
    livreur_id = f"LIVREUR_{num}"
    display_name = f"Livreur {prenom} (# {num})"

    return livreur_id, display_name
