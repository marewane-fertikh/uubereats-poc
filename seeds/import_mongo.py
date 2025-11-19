import json
from pymongo import MongoClient

def importer_collection(db, nom_collection, fichier_json):
    print(f"[INFO] Import de {fichier_json} dans {nom_collection}...")

    with open(fichier_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # On repart propre
    collection = db[nom_collection]
    collection.drop()

    # Insert
    collection.insert_many(data)
    print(f"[OK] {nom_collection} : {len(data)} documents insérés.\n")


def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ubereats"]

    importer_collection(db, "restaurants", "data/restaurants.json")
    importer_collection(db, "menus", "data/menus.json")

    # Index utiles
    print("[INFO] Création des index...")
    db.menus.create_index("restaurant_id")
    db.restaurants.create_index("id")
    print("[OK] Index créés.")
    print("\n[FIN] Import Mongo terminé avec succès !")


if __name__ == "__main__":
    main()
