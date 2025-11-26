# redis_poc/db.py
"""
Utilitaires Redis pour le POC UberEats :
- Connexion à Redis
- Sauvegarde / lecture d'une commande
"""

import json
import redis


def get_redis_connection() -> redis.Redis:
    """
    Retourne une connexion Redis.
    decode_responses=True → on travaille directement avec des str.
    """
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def save_commande(r: redis.Redis, commande_id: str, data: dict) -> None:
    """
    Sauvegarde une commande dans un hash Redis "commandes".
    La valeur est un JSON pour rester flexible.
    """
    r.hset("commandes", commande_id, json.dumps(data))


def read_commande(r: redis.Redis, commande_id: str) -> dict | None:
    """
    Lit une commande dans le hash "commandes".
    Retourne un dict ou None si l'ID n'existe pas.
    """
    raw = r.hget("commandes", commande_id)
    if raw is None:
        return None
    return json.loads(raw)
