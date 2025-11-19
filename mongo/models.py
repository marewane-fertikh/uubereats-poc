# mongo/models.py
"""
Constantes de statuts pour le cycle de vie d'une commande.
On les utilise partout pour éviter les fautes de frappe.
"""

STATUT_CREE = "cree"                    # commande créée par le client
STATUT_A_PREPARER = "a_preparer"        # envoyée au restaurant
STATUT_PRETE = "prete"                  # restaurant a fini
STATUT_ASSIGNEE = "assignee"            # livreur assigné
STATUT_LIVREE = "livree"                # livreur a livré
STATUT_NOTIFIE_CLIENT = "notification_client"  # client notifié

ALL_STATUS = {
    STATUT_CREE,
    STATUT_A_PREPARER,
    STATUT_PRETE,
    STATUT_ASSIGNEE,
    STATUT_LIVREE,
    STATUT_NOTIFIE_CLIENT,
}
