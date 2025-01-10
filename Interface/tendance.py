# tendance.py

import tkinter as tk  
from tkinter import ttk, messagebox  # Fournit des widgets améliorés et des boîtes de dialogue pour tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permet d'intégrer des graphiques matplotlib dans tkinter
import matplotlib.pyplot as plt  # Utilisé pour tracer des graphiques
import backend_  # Importation des fonctions back end pour gérer les données de tendance

# --------------------------- PARTIE 2 : RÉCUPÉRATION DES DONNÉES DE TENDANCE ---------------------------

def update_moyenne(date, trend_labels):
    """
    Met à jour les labels de tendance avec les données récupérées pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les tendances sont affichées.
    :param trend_labels: Dictionnaire contenant les widgets Label pour afficher les informations.
    """
    data = backend_.get_trend_data(date)  # Récupère les données de tendance pour la date donnée
    trend_labels["date"].config(text=f"Date : {date}")
    trend_labels["temp"].config(text=f"Température : {data.get('Température', 'N/A')}°C")
    trend_labels["humidity"].config(text=f"Humidité : {data.get('Humidité', 'N/A')}%")
    trend_labels["co2"].config(text=f"CO2 : {data.get('CO2', 'N/A')} ppm")

# --------------------------- PARTIE 3 : INITIALISATION DE L'INTERFACE TENDANCES ---------------------------

def initialiser_sections_tendances(parent_frame):
    """
    Initialise les sections de l'interface des tendances dans le cadre parent.

    :param parent_frame: Cadre parent dans lequel afficher l'interface des tendances.
    :return: Tuple contenant les cadres `trend_frame` et `trend_info_frame`.
    """
    # Nettoyage des widgets existants dans le cadre parent
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Création du cadre principal pour les tendances
    trend_frame = tk.Frame(parent_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
    trend_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Titre de la section des tendances
    tk.Label(trend_frame, text="Tendances Moyennes en Date du :", font=("Arial", 16, "bold"), bg="#CDCDB4").pack(pady=10)

    # Cadre supérieur pour les informations et les conditions optimales
    top_frame = tk.Frame(trend_frame, bg="#8B8B7A")  
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Cadre pour afficher les informations de tendance
    trend_info_frame = tk.Frame(top_frame, bg="#8B8B7A", relief=tk.GROOVE, borderwidth=2)
    trend_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Cadre pour afficher les conditions optimales
    condition_frame = creer_cadre_conditions(top_frame)
    condition_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    return trend_frame, trend_info_frame

# --------------------------- PARTIE 4 : AJOUT DES WIDGETS INTERACTIFS ---------------------------

def ajouter_widgets_interactifs(trend_frame, trend_info_frame):
    """
    Ajoute les widgets interactifs pour gérer les tendances moyennes.
    Cette partie inclut les sélecteurs de date et de paramètre, ainsi que l'affichage des graphiques.

    :param trend_frame: Cadre principal contenant les éléments visuels des tendances.
    :param trend_info_frame: Cadre contenant les informations détaillées sur les tendances (date, température, humidité, CO2).
    """
    # Création des labels pour afficher les informations de tendance
    trend_labels = {
        "date": tk.Label(trend_info_frame, text="Date : ", font=("Arial", 12), bg="#8B8B7A"),
        "temp": tk.Label(trend_info_frame, text="Température :", font=("Arial", 12), bg="#8B8B7A"),
        "humidity": tk.Label(trend_info_frame, text="Humidité : ", font=("Arial", 12), bg="#8B8B7A"),
        "co2": tk.Label(trend_info_frame, text="CO2 :", font=("Arial", 12), bg="#8B8B7A")
    }

    # Placement des labels dans le cadre d'informations
    trend_labels["date"].grid(row=0, column=0, sticky="w", padx=10, pady=5)
    trend_labels["temp"].grid(row=0, column=1, sticky="w", padx=60, pady=5)
    trend_labels["humidity"].grid(row=1, column=1, sticky="w", padx=60, pady=5)
    trend_labels["co2"].grid(row=2, column=1, sticky="w", padx=60, pady=5)

    def on_date_selected(selected_date):
        """
        Callback appelé lorsqu'une date est sélectionnée. Met à jour les labels de tendance et trace le graphique.

        :param selected_date: Date sélectionnée au format "YYYY-MM-DD".
        """
        selected_parameter = liste_parametres.get()
        backend_.update_moyenne(selected_date, trend_labels)  # Met à jour les labels avec les données de tendance
        tracer_graphique(selected_parameter, bottom_frame, selected_date)  # Trace le graphique correspondant

    # Création du sélecteur de date
    date_selector = creer_selecteur_date(trend_info_frame, on_date_selected)
    date_selector.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    def on_parameter_selected(selected_parameter):
        """
        Callback appelé lorsqu'un paramètre est sélectionné. Trace le graphique correspondant.

        :param selected_parameter: Paramètre sélectionné (Température, Humidité, CO2).
        """
        selected_date = trend_labels["date"].cget("text").split(": ")[1]
        tracer_graphique(selected_parameter, bottom_frame, selected_date)

    # Création du sélecteur de paramètre
    parameter_frame, liste_parametres = creer_selecteur_parametre(trend_frame, on_parameter_selected)
    parameter_frame.pack(pady=5)

    # Cadre pour afficher les graphiques
    bottom_frame = tk.Frame(trend_frame, bg="white", height=400)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# --------------------------- PARTIE 5 : AFFICHAGE DU MENU DES TENDANCES ---------------------------

def afficher_menu_tendances(parent_frame):
    """
    Initialise et affiche le menu des tendances dans le cadre parent.

    :param parent_frame: Cadre parent dans lequel afficher le menu des tendances.
    """
    trend_frame, trend_info_frame = initialiser_sections_tendances(parent_frame)
    ajouter_widgets_interactifs(trend_frame, trend_info_frame)

# --------------------------- PARTIE 6 : SÉLECTION DE LA DATE ---------------------------

def creer_selecteur_date(parent, on_date_selected_callback):
    """
    Crée un sélecteur de date permettant à l'utilisateur de choisir un jour, un mois et une année.

    :param parent: Cadre parent dans lequel les widgets seront ajoutés.
    :param on_date_selected_callback: Fonction de rappel appelée avec la date sélectionnée.
    :return: Cadre contenant les widgets de sélection de date.
    """
    frame = tk.Frame(parent, bg="#8B8B7A")

    # Labels pour les sélecteurs de jour, mois et année
    tk.Label(frame, text="Jour", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=0, padx=5, pady=2)
    tk.Label(frame, text="Mois", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame, text="Année", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=2, padx=5, pady=2)

    # Combobox pour sélectionner le jour
    day_cb = ttk.Combobox(frame, values=[str(i) for i in range(1, 32)], width=4, state="readonly")
    # Combobox pour sélectionner le mois
    month_cb = ttk.Combobox(frame, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], width=6, state="readonly")
    # Combobox pour sélectionner l'année
    year_cb = ttk.Combobox(frame, values=[str(i) for i in range(2020, 2026)], width=6, state="readonly")

    # Placement des combobox dans le cadre
    day_cb.grid(row=1, column=0, padx=5, pady=2)
    month_cb.grid(row=1, column=1, padx=5, pady=2)
    year_cb.grid(row=1, column=2, padx=5, pady=2)

    def on_button_click():
        """
        Gestion de l'événement lorsque le bouton "Afficher" est cliqué.
        Valide les sélections et appelle la fonction de rappel avec la date sélectionnée.
        """
        # Formatage des valeurs sélectionnées avec des zéros devant si nécessaire
        day = day_cb.get().zfill(2)
        month = month_cb.get().zfill(2)
        year = year_cb.get()
        if not (day and month and year):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return
        selected_date = f"{year}-{month}-{day}"
        on_date_selected_callback(selected_date)

    # Bouton pour valider la sélection de la date
    ttk.Button(frame, text="Afficher", command=on_button_click).grid(row=2, column=0, columnspan=3, pady=10)

    return frame

# --------------------------- PARTIE 7 : CONDITIONS OPTIMALES ---------------------------

def creer_cadre_conditions(parent):
    """
    Crée un cadre affichant les conditions optimales de la serre.

    :param parent: Cadre parent dans lequel le cadre des conditions sera ajouté.
    :return: Cadre contenant les informations sur les conditions optimales.
    """
    frame = tk.Frame(parent, bg="palegreen", relief=tk.GROOVE, borderwidth=2)
    tk.Label(frame, text="Conditions Optimales", font=("Arial", 14), bg="palegreen").pack(pady=5)
    tk.Label(frame, text="Température : 20-25°C", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame, text="Humidité : 50-70%", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame, text="CO2 : 350-450 ppm", font=("Arial", 12), bg="palegreen").pack(pady=2)
    return frame

# --------------------------- PARTIE 8 : GRAPHIQUES DYNAMIQUES ---------------------------

def tracer_graphique(parameter, frame, date):
    """
    Trace un graphique de l'évolution d'un paramètre environnemental sur une journée.

    :param parameter: Paramètre environnemental à tracer (Température, Humidité, CO2).
    :param frame: Cadre dans lequel le graphique sera affiché.
    :param date: Date au format "YYYY-MM-DD" pour laquelle le graphique est tracé.
    """
    detailed_data = backend_.get_detailed_trend_data(date)  # Récupère les données détaillées pour la date
    if not detailed_data:
        messagebox.showwarning("Erreur", f"Aucune donnée disponible pour la date {date}.")
        return

    hourly_data = detailed_data
    hours = list(hourly_data.keys())
    values = [hourly_data[hour][parameter] for hour in hours]

    # Nettoyage des widgets existants dans le cadre du graphique
    for widget in frame.winfo_children():
        widget.destroy()

    # Définition des plages critiques, optimales et acceptables pour chaque paramètre
    ranges = {
        "Température": (15, 20, 25, 32),
        "Humidité": (30, 50, 70, 90),
        "CO2": (200, 350, 450, 1800),
    }

    # Récupère les limites bas et haut en fonction du paramètre
    critical_low, optimal_min, optimal_max, critical_high = ranges.get(parameter, (min(values), min(values), max(values), max(values)))

    # Création de la figure et de l'axe pour le graphique
    fig, ax = plt.subplots(figsize=(8, 4))

    # Coloration des plages critiques et optimales
    ax.axhspan(critical_low, optimal_min, color="red", alpha=0.2)     # Zone critique basse
    ax.axhspan(optimal_min, optimal_max, color="green", alpha=0.2)    # Zone optimale
    ax.axhspan(optimal_max, critical_high, color="red", alpha=0.2)    # Zone critique haute
    ax.axhspan(optimal_max, critical_high, color="white", alpha=1)    # Nettoyage de la zone critique haute
    ax.axhspan(critical_low, optimal_min, color="white", alpha=1)     # Nettoyage de la zone critique basse

    # Tracé des valeurs du paramètre
    ax.plot(hours, values, marker='o', color='blue', label=parameter)
    ax.set_title(f"Évolution de {parameter} - {date}", fontsize=14)  # Titre du graphique
    ax.set_xlabel("Heures")  # Label de l'axe X
    ax.set_ylabel(parameter)  # Label de l'axe Y
    ax.grid(True)  # Affichage de la grille
    ax.legend()  # Affichage de la légende

    # Définition des marges pour l'axe Y
    margin = 2
    y_min = max(critical_low - margin, min(values) - margin)
    y_max = min(critical_high + margin, max(values) + margin)
    ax.set_ylim(y_min, y_max)  # Ajustement des limites de l'axe Y

    # Intégration du graphique dans le cadre Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --------------------------- PARTIE 9 : SÉLECTION DU PARAMÈTRE POUR LE GRAPHIQUE ---------------------------

def creer_selecteur_parametre(parent, on_parameter_selected_callback):
    """
    Crée un sélecteur de paramètre environnemental (Température, Humidité, CO2).

    :param parent: Cadre parent dans lequel le sélecteur sera ajouté.
    :param on_parameter_selected_callback: Fonction de rappel appelée avec le paramètre sélectionné.
    :return: Tuple contenant le cadre du sélecteur et le widget Combobox.
    """
    frame = tk.Frame(parent, bg="lightyellow")
    tk.Label(frame, text="Paramètre :", font=("Arial", 12), bg="lightyellow").pack(side=tk.LEFT, padx=5)

    # Combobox pour sélectionner le paramètre
    parameter_cb = ttk.Combobox(frame, values=["Température", "Humidité", "CO2"], state="readonly")
    parameter_cb.set("Température")  # Sélection par défaut
    parameter_cb.pack(side=tk.LEFT, padx=5)

    def on_parameter_change(event):
        """
        Callback appelé lorsqu'un paramètre est sélectionné dans le Combobox.

        :param event: Événement déclenché lors de la sélection.
        """
        selected_parameter = parameter_cb.get()
        on_parameter_selected_callback(selected_parameter)

    # Liaison de l'événement de sélection au callback
    parameter_cb.bind("<<ComboboxSelected>>", on_parameter_change)
    return frame, parameter_cb

# --------------------------- MAIN (Point d'entrée du programme) ---------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion de la Serre Intelligente")
    root.geometry("800x600")
    afficher_menu_tendances(root)  # Affiche le menu des tendances dans la fenêtre principale
    root.mainloop()

