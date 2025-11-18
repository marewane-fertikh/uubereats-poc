from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_mongo_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["uubereats_poc"]
        return db
    except ConnectionFailure as e:
        print("Erreur de connexion MongoDB:", e)
        raise

def creer_commande(db, commande_id, client_id, restaurant_id):
    commande = {
        "_id": commande_id,
        "client_id": client_id,
        "restaurant_id": restaurant_id,
        "livreur_id": None,
        "statut": "cree"
    }
    db.commandes.insert_one(commande)
    return commande

def lire_commande(db, commande_id):
    return db.commandes.find_one({"_id": commande_id})

def mettre_a_jour_statut(db, commande_id, statut, livreur_id=None):
    update = {"statut": statut}
    if livreur_id:
        update["livreur_id"] = livreur_id

    db.commandes.update_one(
        {"_id": commande_id},
        {"$set": update}
    )
