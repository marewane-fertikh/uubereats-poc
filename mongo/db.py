# mongo/db.py
"""
Utilitaires MongoDB pour le POC :
- Connexion au replica set
- CRUD sur les commandes
- Change stream générique filtré en Python
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
import time

from mongo.models import STATUT_CREE


# ---------------------------------------------------------------------------
# Connexion MongoDB
# ---------------------------------------------------------------------------

def get_db():
    """
    Retourne la base 'ubereats' sur le replicaset rs0.
    Assure-toi que mongod est lancé avec ce replicaset.
    """
    client = MongoClient(
        "mongodb://localhost:27017/?replicaSet=rs0",
        uuidRepresentation="standard"
    )
    return client.ubereats


db = get_db()
commandes = db.commandes


# ---------------------------------------------------------------------------
# CRUD commandes
# ---------------------------------------------------------------------------

def creer_commande(restaurant_id: str, menu_id: str, client_id: str) -> str:
    """
    Crée une commande avec statut initial 'cree' et renvoie son _id (str).
    """
    doc = {
        "restaurant_id": restaurant_id,
        "menu_id": menu_id,
        "client_id": client_id,
        "livreur_id": None,
        "statut": STATUT_CREE,
        "timestamp": time.time(),
    }
    result = commandes.insert_one(doc)
    return str(result.inserted_id)


def lire_commande(commande_id: str):
    """
    Retourne le document commande correspondant (ou None).
    """
    return commandes.find_one({"_id": ObjectId(commande_id)})


def mettre_a_jour_statut(
    commande_id: str,
    nouveau_statut: str,
    livreur_id: str | None = None
) -> None:
    """
    Met à jour le champ 'statut' d'une commande.
    Optionnellement met aussi à jour 'livreur_id'.
    """
    update = {"$set": {"statut": nouveau_statut}}
    if livreur_id is not None:
        update["$set"]["livreur_id"] = livreur_id

    commandes.update_one(
        {"_id": ObjectId(commande_id)},
        update,
    )


# ---------------------------------------------------------------------------
# Change stream générique
# ---------------------------------------------------------------------------

def ecouter_evenements(statut_voulu: str, commande_id: str | None = None):
    """
    Générateur qui écoute les changements sur la collection 'commandes'
    via un change stream, et renvoie uniquement les documents dont :

      - doc['statut'] == statut_voulu
      - et, si 'commande_id' est fourni, doc['_id'] == commande_id

    IMPORTANT :
    On ne filtre PAS dans le pipeline Mongo, on filtre en Python.
    Ça évite tous les soucis de 'operationType', etc.
    """

    try:
        with commandes.watch(full_document="updateLookup") as stream:
            info_cmd = f" pour commande {commande_id}" if commande_id else ""
            print(f"[MONGO] En attente d'événements statut='{statut_voulu}'{info_cmd}...")

            for change in stream:
                full_doc = change.get("fullDocument")
                if not full_doc:
                    continue

                # Filtrage Python
                if full_doc.get("statut") != statut_voulu:
                    continue

                if commande_id is not None and str(full_doc["_id"]) != str(commande_id):
                    continue

                yield full_doc

    except PyMongoError as e:
        print(f"[ERREUR MONGO] Change stream interrompu : {e}")
