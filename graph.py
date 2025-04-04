import sqlite3
import pygal
import os

# Connexion à la base de données
conn = sqlite3.connect("/home/elprimooooo/ams/monitoring/monitoring.db")
cursor = conn.cursor()

# Créer le répertoire static s'il n'existe pas
static_output_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'
os.makedirs(static_output_dir, exist_ok=True)

# Créer un fichier HTML pour inclure les graphiques
html_output = os.path.join(static_output_dir, "graphiques_sondes.html")
with open(html_output, 'w') as f:
    # Ajouter la structure de base du fichier HTML
    f.write("<html><head><title>Graphiques des sondes</title></head><body>\n")
    f.write("<h1>Graphiques des sondes</h1>\n")
    
    # Récupérer toutes les sondes distinctes de la base de données
    cursor.execute("SELECT DISTINCT sonde FROM monitoring")
    sondes = cursor.fetchall()

    # Créer un graphique pour chaque sonde et l'enregistrer dans un fichier SVG directement dans static/
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
        
        # Enregistrer le graphique dans un fichier SVG dans le dossier static/
        output_file = os.path.join(static_output_dir, f"{sonde}_graph.svg")
        line_chart.render_to_file(output_file)
        print(f"Graphique pour {sonde} enregistré sous {output_file}")

        # Ajouter le graphique SVG au fichier HTML
        f.write(f"<h2>Graphique de la sonde {sonde}</h2>\n")
        f.write(f'<object data="{os.path.basename(output_file)}" type="image/svg+xml" width="600" height="400"></object>\n')

    # Ajouter la fin du fichier HTML
    f.write("</body></html>\n")

# Fermer la connexion à la base de données
conn.close()

print(f"Fichier HTML généré à {html_output}")
