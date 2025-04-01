import os
import subprocess

# Liste des fichiers SVG générés précédemment
graph_files = [
    "sonde1_graph.svg",
    "sonde2_graph.svg",  # Ajoute ici tous les fichiers SVG générés par le script précédent
    "sonde3_graph.svg"
]

# Vérifier si des fichiers SVG existent
available_files = [file for file in graph_files if os.path.exists(file)]

if not available_files:
    print("Aucun fichier SVG trouvé.")
else:
    # Afficher la liste des fichiers disponibles
    print("Fichiers graphiques disponibles :")
    for idx, file in enumerate(available_files, 1):
        print(f"{idx}. {file}")

    # Demander à l'utilisateur de choisir un fichier
    try:
        choice = int(input(f"\nChoisissez le numéro du fichier à afficher (1-{len(available_files)}): "))
        
        # Vérifier que le choix est valide
        if 1 <= choice <= len(available_files):
            chosen_file = available_files[choice - 1]
            print(f"\nAffichage du graphique pour {chosen_file}...")
            subprocess.run(["w3m", chosen_file])  # Utilise w3m pour afficher le fichier SVG
        else:
            print("Choix invalide. Veuillez sélectionner un numéro valide.")
    except ValueError:
        print("Entrée invalide. Veuillez entrer un numéro valide.")
