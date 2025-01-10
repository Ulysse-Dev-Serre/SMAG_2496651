# backend_alerts.py

import json  # Importation du module JSON pour la gestion de la sérialisation et désérialisation des données

# --------------------------- INITIALISATION DE LA BASE DE DONNÉES DES ALERTES ---------------------------

# Cette structure de données sert à stocker les alertes de manière organisée.
# - "active_alerts" : Liste des alertes actuellement actives.
# - "read_alerts" : Liste des alertes qui ont été lues ou traitées.
# - "alerts_by_time" : Dictionnaire où chaque clé est une heure (format "HH:MM") et la valeur est une alerte associée.

alerts_database = {
    "active_alerts": [],  # Initialisation d'une liste vide pour les alertes actives
    "read_alerts": [],    # Initialisation d'une liste vide pour les alertes lues
    "alerts_by_time": {}   # Initialisation d'un dictionnaire vide pour les alertes par heure
}

# --------------------------- FONCTION : AJOUTER UNE ALERTE PAR HEURE ---------------------------

def add_alert_by_time(hour, parameter, value, message, filename="alerts.json"):
    """
    Ajoute une alerte à une heure spécifique dans la base de données des alertes.

    :param hour: Heure à laquelle l'alerte doit être déclenchée (format "HH:MM").
    :param parameter: Le paramètre environnemental concerné (ex. "Température").
    :param value: La valeur seuil du paramètre qui déclenche l'alerte.
    :param message: Message prédéfini décrivant l'alerte.
    :param filename: Nom du fichier JSON où les alertes sont sauvegardées (par défaut "alerts.json").
    """
    # Charger les alertes existantes depuis le fichier JSON
    load_alerts_from_file(filename)

    # Définir ou mettre à jour l'alerte pour l'heure spécifiée
    alerts_database["alerts_by_time"][hour] = {
        "Parameter": parameter,  # Le paramètre concerné par l'alerte
        "Value": value,          # La valeur seuil qui déclenche l'alerte
        "Message": message,      # Message explicatif de l'alerte
        "read": False            # Indique que l'alerte est nouvelle et non encore lue
    }

    # Sauvegarder les alertes mises à jour dans le fichier JSON
    save_alerts_to_file(filename)

# --------------------------- FONCTION : SAUVEGARDER LES ALERTES DANS LE FICHIER JSON ---------------------------

def save_alerts_to_file(filename="alerts.json"):
    """
    Sauvegarde la base de données des alertes dans un fichier JSON.
    Cette fonction fusionne les données existantes avec les nouvelles données avant de sauvegarder.

    :param filename: Nom du fichier JSON où les alertes sont sauvegardées (par défaut "alerts.json").
    """
    try:
        # Tenter de charger les données existantes du fichier JSON
        try:
            with open(filename, "r") as file:
                existing_data = json.load(file)  # Charger les données existantes
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou est corrompu, initialiser une structure vide
            existing_data = {
                "active_alerts": [],
                "read_alerts": [],
                "alerts_by_time": {}
            }

        # Fusionner les données actuelles avec celles de alerts_database

        # 1. Copier les listes "active_alerts" et "read_alerts" depuis alerts_database
        existing_data["active_alerts"] = alerts_database.get("active_alerts", [])
        existing_data["read_alerts"] = alerts_database.get("read_alerts", [])

        # 2. Fusionner le dictionnaire "alerts_by_time"
        if "alerts_by_time" not in existing_data:
            existing_data["alerts_by_time"] = {}  # Initialiser si absent
        for hour, alert_info in alerts_database["alerts_by_time"].items():
            existing_data["alerts_by_time"][hour] = alert_info  # Ajouter ou mettre à jour l'alerte pour chaque heure

        # Sauvegarder les données fusionnées dans le fichier JSON avec une indentation pour la lisibilité
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)

        # Mettre à jour alerts_database avec les données fusionnées pour assurer la cohérence en mémoire
        alerts_database.update(existing_data)

    except IOError as e:
        # En cas d'erreur lors de la sauvegarde, afficher un message d'erreur
        print(f"Error saving alerts: {e}")

# --------------------------- FONCTION : CHARGER LES ALERTES DU FICHIER JSON ---------------------------

def load_alerts_from_file(filename="alerts.json"):
    """
    Charge les alertes depuis un fichier JSON dans la variable globale alerts_database.
    Si le fichier n'existe pas ou est mal formé, initialise une structure vide.

    :param filename: Nom du fichier JSON à charger (par défaut "alerts.json").
    """
    global alerts_database  # Indique que nous modifions la variable globale alerts_database
    try:
        with open(filename, "r") as file:
            data = json.load(file)  # Charger les données depuis le fichier JSON
        alerts_database = data  # Mettre à jour la base de données des alertes avec les données chargées

        # Vérifier et assurer que la structure minimale existe
        if "alerts_by_time" not in alerts_database:
            alerts_database["alerts_by_time"] = {}
        if "active_alerts" not in alerts_database:
            alerts_database["active_alerts"] = []
        if "read_alerts" not in alerts_database:
            alerts_database["read_alerts"] = []

    except (FileNotFoundError, json.JSONDecodeError):
        # Si le fichier n'existe pas ou est corrompu, réinitialiser la base de données des alertes
        alerts_database = {
            "active_alerts": [],
            "read_alerts": [],
            "alerts_by_time": {}
        }

# --------------------------- FONCTION : RÉCUPÉRER LES ALERTES PAR HEURE ---------------------------

def get_alerts_by_time(filename="alerts.json"):
    """
    Charge les alertes depuis le fichier JSON et renvoie le dictionnaire des alertes classées par heure.

    :param filename: Nom du fichier JSON à charger (par défaut "alerts.json").
    :return: Dictionnaire des alertes organisées par heure.
    """
    load_alerts_from_file(filename)  # Charger les alertes depuis le fichier JSON
    return alerts_database["alerts_by_time"]  # Retourner le dictionnaire des alertes par heure

# --------------------------- FONCTION : RÉCUPÉRER LES ALERTES NON LUES ---------------------------

def get_unread_alerts(filename="alerts.json"):
    """
    Charge les alertes depuis le fichier JSON et renvoie une liste des alertes non lues.

    :param filename: Nom du fichier JSON à charger (par défaut "alerts.json").
    :return: Liste des alertes dont le champ 'read' est False.
    """
    load_alerts_from_file(filename)  # Charger les alertes depuis le fichier JSON
    return [
        alert
        for alert in alerts_database["alerts_by_time"].values()
        if not alert.get("read", False)  # Filtrer les alertes non lues
    ]

# --------------------------- INITIALISATION AU DÉMARRAGE DU PROGRAMME ---------------------------

# Charger les alertes dès le démarrage du programme pour s'assurer que alerts_database est à jour
load_alerts_from_file()


#======================================================================================================================================================================================



#=============================================================================================================
#  si tu veux cette parti pourais etre un autre fichier    backend_trend.py
#=========================================================================================================
import fake_database  # Importation du module back end pour accéder aux données

def get_trend_data(date):
    """
    Récupère les données de tendance pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les tendances sont récupérées.
    :return: Dictionnaire contenant les données de température, humidité et CO2 pour la date donnée.
             Si aucune donnée n'est trouvée, retourne un dictionnaire vide.
    """
    data_list = fake_database.tendance_moyenne()  # Récupère la liste des tendances moyennes
    data = next((item for item in data_list if item["Date"] == date), {})
    return data

def get_detailed_trend_data(date):
    """
    Récupère les données détaillées pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les données détaillées sont récupérées.
    :return: Dictionnaire contenant les données détaillées par heure.
             Si aucune donnée n'est trouvée, retourne un dictionnaire vide.
    """
    detailed_data = fake_database.get_detailed_data()  # Récupère les données détaillées
    return detailed_data.get(date, {})








"""Btw Robens, si tu veux, tu pourras seulement garder cette partie intacte et ça pourrait être suffisant. Je me dis que, comme le prof a interdit
 Mongo et que tu dois recommencer, ça pourrait peut-être aller plus vite.

 Il manque juste un petit détail que je n'arrive pas à régler.
Peut-être que tu pourrais travailler dessus : c'est le fait de détecter les "read alerts", pour que, quand une alerte est lue, on puisse
 annuler la notification c'est un truque par raport au boolen a la ligne 38. 

 J'ai envoiller block par block a GPT pour qu'il me commente ca comme un fou haha donc tu peux suprimer ce qui n'es pas utilise , Quoique ca pourrais bien etre utile pour la présentation
 
 Si tu n'es pas à l'aise avec ce code, tu peux le changer : ça te fera une bonne base pour commencer. 
 aussi je vais t'envoiller ma fake data_base tu pourra la prendre comme tienne et si tu en a l'envie tu pourrais esseiller de travailller sur un code qui pourais capter
 les donner a alex de ces sensor en temp real bred tout les nom des fonction fonctione parfaitement avec l'interface donc c'est ca ca pourrais faciliter les chose"""