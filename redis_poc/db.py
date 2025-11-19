# redis_poc/db.py
import redis
import json
from typing import Optional, Dict, Any

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

COMMANDE_KEY_PREFIX = "commande:"


def get_redis_connection() -> redis.Redis:
    """
    Retourne une connexion Redis.
    decode_responses=True -> on manipule des str, pas des bytes.
    """
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def _commande_key(commande_id: str) -> str:
    return f"{COMMANDE_KEY_PREFIX}{commande_id}"


def initialiser_commande(
    commande_id: str,
    client_id: str,
    restaurant: Dict[str, Any],
    menu: Dict[str, Any],
) -> None:
    """
    Crée une commande dans Redis avec le statut 'cree'.
    On stocke un snapshot simple.
    """
    r = get_redis_connection()
    r.hset(
        _commande_key(commande_id),
        mapping={
            "commande_id": commande_id,
            "client_id": client_id,
            "restaurant_id": restaurant["restaurant_id"],
            "restaurant_name": restaurant["restaurant_name"],
            "menu_id": menu["menu_id"],
            "menu_name": menu["menu_name"],
            "livreur_id": "",
            "statut": "cree",
        },
    )


def mettre_a_jour_statut(
    commande_id: str,
    statut: str,
    livreur_id: Optional[str] = None,
) -> None:
    """
    Met à jour le statut (et éventuellement le livreur) de la commande.
    """
    r = get_redis_connection()
    values: Dict[str, Any] = {"statut": statut}
    if livreur_id is not None:
        values["livreur_id"] = livreur_id
    r.hset(_commande_key(commande_id), mapping=values)


def lire_commande(commande_id: str) -> Dict[str, str]:
    """
    Lit la commande sous forme de dict Python (pour affichage/debug).
    """
    r = get_redis_connection()
    return r.hgetall(_commande_key(commande_id))


def publier_event(channel: str, payload: dict) -> None:
    """
    Publie un évènement (dict) au format JSON sur un channel Redis.
    """
    r = get_redis_connection()
    msg = json.dumps(payload, ensure_ascii=False)
    r.publish(channel, msg)
    print(f"[REDIS] publish -> {channel}: {msg}")
