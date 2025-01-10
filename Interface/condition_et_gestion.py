import re
import json
import tkinter as tk
from tkinter import ttk

# Bibliothèques nécessaires aux jauges circulaires
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Importer le fichier de alex
"""exemple : from capteur import condition_actuel """
# -----------------------------------------------------------------------------
# Petite fonction utilitaire pour extraire les nombres d'une chaîne contenant
# des unités (°C, %, ppm, lux, etc.).
# Exemple: "28°C" -> "28" -> 28.0
#          "55%"  -> "55" -> 55.0
# -----------------------------------------------------------------------------
def extract_number(value_str):
    """
    Retire tout ce qui n'est pas un chiffre ou un point décimal.
    Retourne 0.0 si le résultat est vide.
    """
    cleaned = re.sub(r"[^\d.]", "", value_str)  # Supprime tous les caractères sauf les chiffres et '.'
    return float(cleaned) if cleaned else 0.0

# -----------------------------------------------------------------------------
# PARTIE 1 : AFFICHAGE DES CONDITIONS ACTUELLES
# -----------------------------------------------------------------------------
    """
    Vide le cadre principal (main_frame), crée un cadre supérieur (top_frame)
    pour afficher les informations de condition (température, humidité, etc.),
    crée un autre cadre (parameter_frame) pour lister chaque paramètre,
    crée un cadre pour le graphique (graph_frame), puis met à jour les conditions.
    Enfin, ajoute trois jauges circulaires (température, humidité, CO2).

    Modification demandée :
     - Séparer le top_frame en deux frames (gauche et droite).
     - top_frame_left : contient la grille de paramètres comme avant.
     - top_frame_right : contient 3 "boutons de volume" (ici, des tk.Scale)
       pour Irrigation, Lumière et Ventilation avec 4 niveaux (0,1,2,3).
    """
def display_condition_screen(main_frame):

    # On détruit tous les widgets précédemment placés dans main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Titre principal - thème foncé
    tk.Label(main_frame, text="Conditions Actuelles", font=("Arial", 16, "bold"), bg="#303030", fg="#ffffff").pack(pady=10, fill=tk.X)

    # Cadre supérieur global (top_frame)
    top_frame = tk.Frame(main_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    # =================== NOUVEAU : deux frames à l'intérieur de top_frame ===================
    # 1) Frame de gauche (top_frame_left) pour afficher les paramètres
    top_frame_left = tk.Frame(top_frame, bg="#8B8B7A")
    top_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 2) Frame de droite (top_frame_right) pour afficher les 3 boutons/volumes
    top_frame_right = tk.Frame(top_frame, bg="#8B8B7A")
    top_frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    # ==========================================================================================

# --------------------------------- PARTIE GAUCHE : PARAMÈTRES (TEMPÉRATURE, HUMIDITÉ, ETC.) ------------------------------------------------------
    parameter_frame = top_frame_left  # On place directement nos labels dans top_frame_left
    # Exemple de données par défaut (avant mise à jour depuis data.json)                      
    parameters = {                        # importation des donner d'alex parameters = condition_actuel()
        "Température": "28°C",         
        "Humidité": "55%",
        "CO2": "420 ppm",
        "Luminosité": "300 lux",
        "Ventilation": "Active",
        "Irrigation": "Off"
    }
#=====================================================================================================================
# ----------------------------------- PARTIE INTERACTIVE (ALEX) --------------------------------------
#====================================================================================================================
# Exemple de code interactif pour la ventilation :
# Tu peux utiliser cette ligne pour lier l'échelle de ventilation à une fonction qui gère l'état de la ventilation.
# Exemple :
# ventilation_scale.bind("<Motion>", lambda event: control_ventilation(ventilation_scale.get()))
#
# Fonction que tu pourrais définir pour gérer l'état de la ventilation selon la valeur de l'échelle :
# def control_ventilation(value):
#     if value == 0:
#         print("Ventilation OFF")  # Eteindre la ventilation
#     elif value == 1:
#         print("Ventilation LOW")  # Ventilation faible
#     elif value == 2:
#         print("Ventilation MEDIUM")  # Ventilation moyenne
#     elif value == 3:
#         print("Ventilation HIGH")  # Ventilation forte                                                                              

    for i, (param, value) in enumerate(parameters.items()): 
        tk.Label(parameter_frame, text=f"{param} :", font=("Arial", 12), bg="#8B8B7A", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        tk.Label(parameter_frame, text=value, font=("Arial", 12), bg="#CDCDB4", fg="#292421").grid(row=i, column=1, sticky="w", padx=10, pady=5)

    irrigation_scale = tk.Scale(top_frame_right, from_=0, to=3, orient=tk.HORIZONTAL, label="Irrigation", bg="#8B8B7A", fg="#000000", troughcolor="#D0D0D0", highlightthickness=0)
    irrigation_scale.pack(padx=10, pady=10, fill=tk.X)

    lumiere_scale = tk.Scale(top_frame_right, from_=0, to=3, orient=tk.HORIZONTAL, label="Lumière", bg="#8B8B7A", fg="#000000", troughcolor="#D0D0D0", highlightthickness=0)
    lumiere_scale.pack(padx=10, pady=10, fill=tk.X)

    ventilation_scale = tk.Scale(top_frame_right, from_=0, to=3, orient=tk.HORIZONTAL, label="Ventilation", bg="#8B8B7A", fg="#000000", troughcolor="#D0D0D0", highlightthickness=0)
    ventilation_scale.pack(padx=10, pady=10, fill=tk.X)

    # --------------------------------------------------------------------------------------------------------------

    # Cadre pour le "graphique simplifié"
    graph_frame = tk.Frame(main_frame, bg="lightgrey", relief=tk.GROOVE, borderwidth=2)
    graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(graph_frame, text="Graphique simplifié en développement", font=("Arial", 12), bg="lightgrey").pack(pady=20)


    # On appelle la mise à jour des conditions (réelles) depuis data.json
    update_conditions(parameter_frame)

    # -------------------------- PARTIE 1.1 : AJOUT DES JAUGES CIRCULAIRES (dans graph_frame) ------------------------------
    gauges_frame = tk.Frame(graph_frame, bg="#1E1E1E")
    gauges_frame.pack(fill=tk.X, padx=20, pady=20)

    # Palettes de couleurs (déjà mentionnées)
    temp_colors = [
        '#00FF00',  # Vert
        '#80FF00',  # Vert-jaune clair
        '#FFFF00',  # Jaune
        '#FF8000',  # Orange
        '#FF0000'   # Rouge
    ]

    # De plus clair (#E0FFFF) à plus foncé (#00008B)
    humidity_colors = [
        '#E0FFFF',  # bleu très pâle (Light Cyan)
        '#ADD8E6',  # bleu clair (Light Blue)
        '#87CEEB',  # bleu ciel (Sky Blue)
        '#4682B4',  # bleu acier (Steel Blue)
        '#00008B'   # bleu foncé (Dark Blue)
    ]

    # De blanc (#FFFFFF) vers noir (#000000)
    co2_colors = [
        '#FFFFFF',  # Blanc
        '#D9D9D9',  # Gris clair
        '#B3B3B3',  # Gris moyen
        '#4D4D4D',  # Gris foncé
        '#000000'   # Noir
    ]

    # Création des trois jauges : Température, Humidité, CO2
    create_modern_gauge(gauges_frame, "Température", parameters["Température"], 15, 35, temp_colors)
    create_modern_gauge(gauges_frame, "Humidité", parameters["Humidité"], 0, 100, humidity_colors)
    create_modern_gauge(gauges_frame, "CO2", parameters["CO2"], 300, 800, co2_colors)

# ------------------------------------PARTIE 2 : MISE À JOUR DES CONDITIONS (lecture de data.json)------------------------------

def update_conditions(parameter_frame): # Alex, si tu exportes des données dans un fichier JSON, sinon on peut les importer directement dans mon code en temps réel (ce qui est plus simple je pense). Dis-moi ce que tu préfères.

    """
    Essaie de lire un fichier data.json pour mettre à jour les paramètres
    (Température, Humidité, CO2, etc.). En cas d'erreur (fichier introuvable,
    JSON invalide), on ignore simplement l'update.
    """
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            real_data = json.load(file)

        # Mettre à jour les labels existants (colonne 1) avec les nouvelles valeurs
        for i, (param, value) in enumerate(real_data.items()):
            parameter_frame.grid_slaves(row=i, column=1)[0].config(text=value)

    except FileNotFoundError:
        print("Fichier de données non trouvé. Les données ne peuvent pas être mises à jour.")
    except json.JSONDecodeError:
        print("Erreur de décodage du fichier JSON. Assurez-vous que le fichier est valide.")

    # On rappelle cette fonction toutes les 10 secondes
    parameter_frame.after(10000, update_conditions, parameter_frame)

# -----------------------------------------------------------------------------
# Fonction de création d'une jauge circulaire "moderne"
# -----------------------------------------------------------------------------
def create_modern_gauge(frame, title, value, min_val, max_val, colors):
    """
    Crée une jauge circulaire de style "futuriste/dark theme" dans 'frame'.
      - title : nom de la jauge (ex: "Température")
      - value : valeur actuelle (peut être un string "28°C" ou un float)
      - min_val, max_val : limites min et max de la jauge
      - colors : liste de couleurs pour dégrader le remplissage
    """

    # On crée un petit Frame pour loger la jauge
    gauge_frame = tk.Frame(frame, bg="#1E1E1E")
    gauge_frame.pack(pady=10, padx=10, side=tk.LEFT)

    # Création d'une figure matplotlib "en polar" (jauge circulaire)
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#1E1E1E')  # Couleur de fond de la figure
    ax.set_facecolor('#1E1E1E')         # Couleur de fond de la zone de tracé

    # Conversion de la valeur en nombre, même si c'est "28°C"
    if isinstance(value, str):
        value_num = extract_number(value)
    else:
        value_num = float(value)

    # On crée une série d'angles pour tracer des arcs colorés
    angles = np.linspace(0, 270, len(colors))
    angles = np.deg2rad(angles)  # Conversion degrés -> radians

    # On remplit des sections entre 0.7 et 0.9 (pour dessiner un anneau)
    for i in range(len(colors) - 1):
        ax.fill_between([angles[i], angles[i+1]], 0.7, 0.9,
                        color=colors[i], alpha=0.6)

    # Placement des "ticks" (graduations) de 0 à 270°, ici on en met 6
    tick_angles = np.linspace(0, 270, 6)  # angles en degrés
    tick_values = np.linspace(min_val, max_val, 6)
    ax.set_xticks(np.deg2rad(tick_angles))
    ax.set_xticklabels([f'{int(v)}' for v in tick_values], color='white')

    # Calcul de l'angle de l'aiguille selon la proportion
    needle_angle = 270 * (value_num - min_val) / (max_val - min_val)
    needle_angle = np.deg2rad(needle_angle)

    # Tracé de l'aiguille (de l'origine vers 0.8)
    ax.plot([0, needle_angle], [0, 0.8], color='white', linewidth=2)

    # Configuration du rayon
    ax.set_ylim(0, 1)

    # Titre de la jauge
    ax.set_title(f"{title}\n{value}", color='white', pad=20)

    # Suppression du quadrillage et des ticks radiaux
    ax.grid(False)
    ax.set_rticks([])

    # On intègre la figure matplotlib dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=gauge_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    return gauge_frame


#------------------ TEST LOCAL : si on exécute ce fichier directement-----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test - Conditions Actuelles")
    root.geometry("800x600")

    main_frame = tk.Frame(root, bg="silver", relief=tk.SUNKEN, borderwidth=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Afficher l'écran des conditions
    display_condition_screen(main_frame)

    # Boucle principale de Tkinter
    root.mainloop()
