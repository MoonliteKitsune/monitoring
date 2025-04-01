import sqlite3
import pygal
import os
import webbrowser

# Connexion à la base de données
conn = sqlite3.connect("/home/elprimooooo/ams/monitoring/monitoring.db")
cursor = conn.cursor()

# Récupérer toutes les sondes distinctes de la base de données
cursor.execute("SELECT DISTINCT sonde FROM monitoring")
sondes = cursor.fetchall()

# Créer un graphique pour chaque sonde
for sonde_tuple in sondes:
    sonde = sonde_tuple[0]  # Extraire le nom de la sonde de la tuple
    
    # Récupérer les valeurs de la sonde dans la base de données
    cursor.execute("SELECT timestamp, valeur FROM monitoring WHERE sonde = ?", (sonde,))
    data = cursor.fetchall()
    
    # Extraire les valeurs et les dates pour le graphique
    dates = [row[0] for row in data]  # Liste des timestamps
    valeurs = [row[1] for row in data]  # Liste des valeurs de la sonde
    
    # Créer un graphique de type Line (courbe)
    line_chart = pygal.Line()
    line_chart.title = f'Graphique de la sonde {sonde}'
    
    # Ajouter les données au graphique
    line_chart.add(sonde, valeurs)
    
    # Enregistrer le graphique dans un fichier SVG
    output_file = f"{sonde}_graph.svg"
    line_chart.render_to_file(output_file)
    
    # Ouvrir le fichier SVG dans le navigateur
    webbrowser.open('file://' + os.path.realpath(output_file))

# Fermer la connexion à la base de données
conn.close()
