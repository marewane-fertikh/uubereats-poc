# mongo/db.py
from pymongo import MongoClient
import os

# URI par défaut : replica set local déjà configuré (rs0)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://127.0.0.1:27017/?replicaSet=rs0"
)


_client = MongoClient(MONGO_URI)
_db = _client["ubereats"]


def get_db():
    """Retourne la base de données ubereats."""
    return _db


def get_collection(name: str):
    """Raccourci pour récupérer une collection."""
    return _db[name]
