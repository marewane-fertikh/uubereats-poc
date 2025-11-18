# redis/db.py
import redis
import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

COMMANDE_KEY_PREFIX = "commande:"


def get_redis_connection():
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


def initialiser_commande(commande_id: str, client_id: str, restaurant_id: str):
    """
    Crée une commande dans Redis avec le statut 'cree'.
    On stocke une structure très simple dans un hash.
    """
    r = get_redis_connection()
    r.hset(
        _commande_key(commande_id),
        mapping={
            "commande_id": commande_id,
            "client_id": client_id,
            "restaurant_id": restaurant_id,
            "livreur_id": "",
            "statut": "cree",
        },
    )


def mettre_a_jour_statut(commande_id: str, statut: str, livreur_id: str | None = None):
    """
    Met à jour le statut (et éventuellement le livreur) de la commande.
    """
    r = get_redis_connection()
    values = {"statut": statut}
    if livreur_id is not None:
        values["livreur_id"] = livreur_id
    r.hset(_commande_key(commande_id), mapping=values)


def lire_commande(commande_id: str) -> dict:
    """
    Lit la commande sous forme de dict Python (pour affichage/debug).
    """
    r = get_redis_connection()
    data = r.hgetall(_commande_key(commande_id))
    return data


def publier_event(channel: str, payload: dict):
    """
    Publie un évènement (dict) au format JSON sur un channel Redis.
    """
    r = get_redis_connection()
    r.publish(channel, json.dumps(payload))
