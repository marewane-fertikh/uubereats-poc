# 🍔 UberEats-PoC — Simulation distribuée avec MongoDB (Change Streams) et Redis (Pub/Sub)

Projet réalisé dans le cadre de la ressource **Nouveaux Paradigmes de Bases de Données** (BUT3 Informatique).  
Comparaison de deux technologies NoSQL dans un scénario complet inspiré d’Uber Eats :

- **MongoDB** via les *Change Streams* (suivi temps réel + persistance)
- **Redis** via *Publish/Subscribe* (diffusion instantanée d’événements)

**Pipeline simulé :**  
`Client → Restaurant → Plateforme → Livreur → Client`

L’objectif est de montrer deux approches du temps réel, de mesurer leur comportement,  
et de comprendre leurs cas d’usage respectifs.

---

## 📁 Structure du projet

```
uubereats-poc/
├── data -> data_local/
├── data_local/       # dataset Kaggle (restaurants + menus)
├── mongo/            # Implémentation MongoDB Change Streams
│   ├── acteurs/
│   ├── models.py
│   ├── db.py
│   └── ...
├── redis_poc/        # Implémentation Redis Pub/Sub
│   ├── acteurs/
│   ├── data_loader.py
│   ├── db.py
│   ├── logger.py
│   └── ...
└── tools/            # Scripts (conversion CSV → JSON, etc.)
```

> ⚠️ Les fichiers Kaggle sont volumineux. Ils sont stockés dans `data_local/`  
> et un lien symbolique `data/` permet de les utiliser sans les commiter dans Git.

---

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/<username>/uubereats-poc.git
cd uubereats-poc
```

### 2. Préparer l’environnement Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Activer MongoDB (Replica Set obligatoire)

MongoDB Change Streams nécessitent un Replica Set, même en local.

```bash
sudo systemctl stop mongod
sudo systemctl start mongod --replSet rs0
mongosh
> rs.initiate()
```

Vérification :
```bash
mongosh --eval "rs.status()"
```

---

## 🍃 Lancer le PoC MongoDB (4 acteurs)

Chaque acteur doit être lancé dans un terminal distinct.

- **Terminal 1 — Client**
  ```bash
  python -m mongo.acteurs.client
  ```
- **Terminal 2 — Restaurant**
  ```bash
  python -m mongo.acteurs.restaurant
  ```
- **Terminal 3 — Plateforme**
  ```bash
  python -m mongo.acteurs.plateforme
  ```
- **Terminal 4 — Livreur**
  ```bash
  python -m mongo.acteurs.livreur
  ```

Le client utilise un Change Stream pour détecter automatiquement la fin du cycle.  
Pour relire l’historique d’une commande :
```bash
python -m mongo.acteurs.timeline <order_id>
```

---

## 🔴 Lancer le PoC Redis (Pub/Sub)

Redis diffuse les événements instantanément entre les acteurs.

- **Terminal 1 — Client**
  ```bash
  python -m redis_poc.acteurs.client
  ```
- **Terminal 2 — Restaurant**
  ```bash
  python -m redis_poc.acteurs.restaurant
  ```
- **Terminal 3 — Plateforme**
  ```bash
  python -m redis_poc.acteurs.plateforme
  ```
- **Terminal 4+ — Livreur(s)**
  ```bash
  python -m redis_poc.acteurs.livreur
  ```

Chaque terminal utilise des logs colorés pour visualiser clairement :
- Client = cyan  
- Plateforme = magenta  
- Restaurant = jaune  
- Livreur = vert

---

## 📊 Architecture simulée

Le pipeline respecte le diagramme de séquence du projet :

```
Client → commande_créée → Restaurant  
Restaurant → commande_prête → Plateforme  
Plateforme → commande_assignée → Livreur  
Livreur → commande_livrée → Plateforme → Client
```

---

## 📈 Résumé technique

### MongoDB
- ✔ Change Streams pour notifier les mises à jour
- ✔ Persistance durable des documents
- ✔ Historisation complète dans `orders_events`
- ✔ Très fiable mais plus lent que Redis

### Redis
- ✔ Latence ultra-faible (< 1 ms)
- ✔ Diffusion immédiate des événements
- ✔ Simple, lisible et parfait pour le temps réel
- ✘ Pas de persistance durable

---

## 📚 Rapport complet

Le rapport PDF associé au projet (22 pages) est disponible ici :  
**👉 Du_dataset_Kaggle_a_la_simulation_distribuee.pdf**

Il contient :
- l’analyse technique,
- l’architecture,
- les résultats des tests,
- la comparaison MongoDB / Redis,
- les difficultés rencontrées,
- les perspectives.

---

## 🧑‍💻 Auteur

Projet réalisé par **Marewane Fertikh**  
BUT3 Informatique – IUT de Villetaneuse  
Ressource : Nouveaux Paradigmes de Bases de Données

---

## ✔️ Licence

Ce projet est libre à des fins pédagogiques.  
**MIT License**

---

## 💬 Questions / remarques

Pour toute remarque ou demande d’information :  
📧 marewane.fertikh@edu.univ-paris13.fr

