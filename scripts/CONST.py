"""CONST.py: Constantes' definition."""

API_PATH = "http://127.0.0.1:8000"

PAGES = ["Utilisateur", "Administrateur"]

USER_OPTIONS = [
    "Tableau de bord",
    "Ajouter un message",
    "Modifier le message du jour",
    "Lire un message à une date précise",
]

ADMIN_OPTIONS = [
    "Lister utilisateurs",
    "Ajouter utilisateur",
    "Modifier utilisateur",
    "Supprimer utilisateur",
    "Mood of the day",
    "Mean mood"
]

NO_POST = "Pas de message"
NO_USER = "Pas d'utilisateur"
POST_ID_NOT_EXISTS = "L'ID message n'existe pas"
POST_ADDED = "Message ajouté"
POST_EDITED = "Message modifié"
POST_DELETED = "Message supprimé"
NOT_DIGIT= "Veuillez entrer un nombre"
USER_NOT_EXISTS = "L'utilisateur n'existe pas"
EMAIL_ALREADY_EXISTS = """
    L'adresse email est déjà utilisée.
    Veuillez en renseigné une nouvelle.
"""
POST_ALREADY_EXISTS = """
    Le message du jour a déjà été renseigné.
    Vous pouvez le modifier via l'onglet "Modifier le message du jour".
"""
USER_ADDED = "Utilisateur ajouté"
USER_EDITED = "Utilisateur modifié"
USER_DELETED = "Utilisateur supprimé"
