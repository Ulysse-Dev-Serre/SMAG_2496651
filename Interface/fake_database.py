import json  # Pour gérer la sauvegarde dans un fichier JSON



# Le code qui sert à récolter ces données n'existe pas encore. Donc, peut-être que nous pouvons continuer à garder cette base de données et, en même temps, essayer
# de développer un code pour récupérer les données des capteurs d'Alex.

# --------------------------- PARTIE 1 : TENDANCES MOYENNES ---------------------------
"""
Cette section fournit des fonctions pour simuler les données environnementales moyennes et détaillées.
"""

def tendance_moyenne():
    """
    Simule l'accès aux données de la base de données.
    :return: Liste de dictionnaires contenant les données environnementales.
    """
    return [
        {"Date": "2024-01-01", "Température": 21.8, "Humidité": 55, "Lumière": 366.67, "CO2": 390},
        {"Date": "2024-01-02", "Température": 21.17, "Humidité": 58, "Lumière": 390, "CO2": 390},
        {"Date": "2024-01-03", "Température": 22.67, "Humidité": 57.33, "Lumière": 443.33, "CO2": 403.33},
        {"Date": "2024-01-04", "Température": 20.5, "Humidité": 56.67, "Lumière": 363.33, "CO2": 386.67},
        {"Date": "2024-01-05", "Température": 22.0, "Humidité": 60, "Lumière": 400, "CO2": 400},
        {"Date": "2024-01-06", "Température": 23.0, "Humidité": 55, "Lumière": 450, "CO2": 410},
        {"Date": "2024-01-07", "Température": 19.5, "Humidité": 62, "Lumière": 300, "CO2": 380},
        {"Date": "2024-01-08", "Température": 21.8, "Humidité": 56, "Lumière": 360, "CO2": 390},
        {"Date": "2024-01-09", "Température": 22.4, "Humidité": 58, "Lumière": 380, "CO2": 395},
        {"Date": "2024-01-10", "Température": 23.5, "Humidité": 54, "Lumière": 440, "CO2": 400},
    ]

def get_detailed_data():
    """
    Simule des données détaillées pour chaque paramètre, indexées par heure.
    :return: Dictionnaire contenant les données par jour et par heure.
    """
    return {
        "2024-01-01": {
            "00:00": {"Température": 21.0, "Humidité": 55, "Lumière": 300, "CO2": 380},
            "04:00": {"Température": 21.5, "Humidité": 56, "Lumière": 350, "CO2": 390},
            "08:00": {"Température": 22.0, "Humidité": 57, "Lumière": 400, "CO2": 400},
            "12:00": {"Température": 21.8, "Humidité": 58, "Lumière": 450, "CO2": 410},
            "16:00": {"Température": 22.2, "Humidité": 57, "Lumière": 400, "CO2": 400},
            "20:00": {"Température": 20.5, "Humidité": 56, "Lumière": 350, "CO2": 390},
        },
        "2024-01-02": {
            "00:00": {"Température": 20.8, "Humidité": 58, "Lumière": 320, "CO2": 390},
            "04:00": {"Température": 21.2, "Humidité": 59, "Lumière": 360, "CO2": 395},
            "08:00": {"Température": 21.5, "Humidité": 60, "Lumière": 390, "CO2": 400},
            "12:00": {"Température": 21.0, "Humidité": 61, "Lumière": 400, "CO2": 405},
            "16:00": {"Température": 20.5, "Humidité": 60, "Lumière": 380, "CO2": 400},
            "20:00": {"Température": 20.0, "Humidité": 58, "Lumière": 350, "CO2": 390},
        },
    }


