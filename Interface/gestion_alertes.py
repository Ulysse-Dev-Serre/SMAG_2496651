# gestion_alertes.py

import tkinter as tk
from tkinter import ttk
from backend_ import add_alert_by_time, get_alerts_by_time, save_alerts_to_file, get_unread_alerts

# --------------------------- PARTIE 1 : FONCTIONS POUR LA GESTION DES ALERTES ---------------------------

def creer_fenetre_alertes():        #backend_alerts
    """
    Crée une fenêtre pour afficher et gérer les alertes.
    """
    fenetre_alertes = tk.Toplevel()
    fenetre_alertes.title("Voir les alertes")
    fenetre_alertes.geometry("400x400")
    fenetre_alertes.configure(bg="#8B8B7A")

    frame_alertes = tk.Frame(fenetre_alertes, bg="#8B8B7A")
    frame_alertes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Création d'un menu local pour ajouter des alertes
    menu_local = tk.Menu(fenetre_alertes)
    fenetre_alertes.config(menu=menu_local)
    menu_local.add_command(label="Ajouter une alerte", command=lambda: ajouter_alerte(fenetre_alertes, frame_alertes))

    # Affichage initial des alertes
    rafraichir_alertes(frame_alertes)

def rafraichir_alertes(frame_alertes):
    """
    Met à jour dynamiquement l'affichage des alertes dans un cadre spécifique.
    """
    count = 0
    # Supprimer les widgets existants
    for widget in frame_alertes.winfo_children():
        widget.destroy()
    alertes = get_alerts_by_time()

    if alertes:
        for heure, alerte in alertes.items():
            count += 1
            tk.Label(
                frame_alertes, 
                text=f"{heure} - {alerte['Parameter']}: {alerte['Value']} ({alerte['Message']})", 
                wraplength=350, 
                bg="#CDCDB4", 
                relief=tk.GROOVE, 
                padx=5, 
                pady=5
            ).pack(fill=tk.X, pady=2)
    else:
        tk.Label(frame_alertes, text="Aucune alerte enregistrée.", bg="#CDCDB4", pady=20).pack()

def ajouter_alerte(fenetre_parent, frame_alertes):
    """
    Ouvre une nouvelle fenêtre pour ajouter une alerte.
    """
    fenetre_ajout = tk.Toplevel(fenetre_parent)
    fenetre_ajout.title("Ajouter une alerte")
    fenetre_ajout.geometry("400x400")
    fenetre_ajout.configure(bg="#8B8B7A")

    ttk.Label(fenetre_ajout, text="(Heure:Min):").pack(pady=5) 
    cadre_temps = tk.Frame(fenetre_ajout, bg="#8B8B7A")
    cadre_temps.pack(pady=5)

    # Création des combobox pour heure et minute
    heures = [f"{i:02}" for i in range(24)]        
    minutes = [f"{i:02}" for i in range(60)]
    combobox_heure = ttk.Combobox(cadre_temps, values=heures, state="readonly", width=5)
    combobox_minute = ttk.Combobox(cadre_temps, values=minutes, state="readonly", width=5)
    combobox_heure.grid(row=0, column=0, padx=5)
    combobox_minute.grid(row=0, column=1, padx=5)

    # Création du champ de sélection pour le paramètre
    ttk.Label(fenetre_ajout, text="Paramètre:").pack(pady=5)
    parametres = ["Température", "Humidité", "CO2"]
    combobox_parametre = ttk.Combobox(fenetre_ajout, values=parametres, state="readonly")
    combobox_parametre.pack(pady=5)

    # Création du champ d'entrée pour la valeur
    ttk.Label(fenetre_ajout, text="Valeur:").pack(pady=5)
    valeur_entree = tk.Entry(fenetre_ajout)
    valeur_entree.pack(pady=5)

    # Création du champ de sélection pour le message prédéfini
    ttk.Label(fenetre_ajout, text="Message prédéfini:").pack(pady=5)
    combobox_message = ttk.Combobox(fenetre_ajout, state="readonly")    
    combobox_message.pack(pady=5)

    # Mise à jour des options du message en fonction du paramètre sélectionné
    def mettre_a_jour_message(event):
        parametre_selectionne = combobox_parametre.get()
        if parametre_selectionne == "Température":
            combobox_message["values"] = ["Température trop élevée", "Température trop basse"]
        elif parametre_selectionne == "Humidité":
            combobox_message["values"] = ["Humidité trop élevée", "Humidité trop basse"]
        elif parametre_selectionne == "CO2":
            combobox_message["values"] = ["CO2 trop élevé", "CO2 trop bas"]
        combobox_message.set("") 

    combobox_parametre.bind("<<ComboboxSelected>>", mettre_a_jour_message) 

    # Validation des données et ajout de l'alerte
    def valider_alerte():
        heure = combobox_heure.get()
        minute = combobox_minute.get()
        parametre = combobox_parametre.get()
        valeur = valeur_entree.get()
        message_predefini = combobox_message.get()

        if heure and minute and parametre and valeur and message_predefini:
            try:
                valeur_flottante = float(valeur)
                add_alert_by_time(f"{heure}:{minute}", parametre, valeur_flottante, message_predefini)
                rafraichir_alertes(frame_alertes)
                fenetre_ajout.destroy()  # Fermer la fenêtre après ajout
            except ValueError:
                error_label = tk.Label(fenetre_ajout, text="La valeur doit être un nombre valide.", fg="red", bg="#8B8B7A")
                error_label.pack(pady=5)
        else:
            error_label = tk.Label(fenetre_ajout, text="Tous les champs doivent être remplis.", fg="red", bg="#8B8B7A")
            error_label.pack(pady=5)

    tk.Button(fenetre_ajout, text="Ajouter", command=valider_alerte).pack(pady=20)  






