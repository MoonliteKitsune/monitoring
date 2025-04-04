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
    # Ajouter la structure de base du fichier HTML avec du CSS pour le style
    f.write("<html><head><title>Graphiques des sondes</title>\n")
    f.write("<style>\n")
    f.write("body { font-family: Arial, sans-serif; background-color: #f4f7f9; color: #333; margin: 0; padding: 0; }\n")
    f.write("h1 { text-align: center; color: #4CAF50; margin-top: 30px; }\n")
    f.write("h2 { color: #4CAF50; }\n")
    f.write("table { width: 80%; margin: 20px auto; border-collapse: collapse; }\n")
    f.write("th, td { padding: 12px 20px; text-align: left; border: 1px solid #ddd; }\n")
    f.write("th { background-color: #4CAF50; color: white; }\n")
    f.write("tr:nth-child(even) { background-color: #f2f2f2; }\n")
    f.write("tr:hover { background-color: #ddd; }\n")
    f.write("object { display: block; margin: 20px auto; border: none; }\n")
    f.write(".container { width: 90%; max-width: 1200px; margin: 0 auto; }\n")
    f.write(".alert-message { background-color: #ffcc00; padding: 15px; margin: 20px 0; text-align: center; border-radius: 5px; }\n")
    f.write("</style>\n")
    f.write("</head><body>\n")
    
    f.write("<div class='container'>\n")
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
        
        # Enregistrer le graphique dans un fichier SVG directement dans le dossier static/
        output_file = os.path.join(static_output_dir, f"{sonde}_graph.svg")
        line_chart.render_to_file(output_file)
        print(f"Graphique pour {sonde} enregistré sous {output_file}")

        # Ajouter le graphique SVG au fichier HTML
        f.write(f"<h2>Graphique de la sonde {sonde}</h2>\n")
        f.write(f'<object data="/static/{os.path.basename(output_file)}" type="image/svg+xml" width="600" height="400"></object>\n')

    # Récupérer la dernière alerte depuis la base de données
    cursor.execute("SELECT * FROM alerte ORDER BY id DESC LIMIT 1")
    alerte = cursor.fetchone()

    if alerte:
        # Ajouter un tableau HTML pour afficher la dernière alerte
        f.write("<h2>Dernière Alerte</h2>\n")
        f.write("<table>\n")
        f.write("<tr><th>Date</th><th>Référence</th><th>Titre</th><th>Status</th></tr>\n")
        f.write(f"<tr><td>{alerte[1]}</td><td>{alerte[2]}</td><td>{alerte[3]}</td><td>{alerte[4]}</td></tr>\n")
        f.write("</table>\n")
    else:
        f.write("<div class='alert-message'>Aucune alerte trouvée.</div>\n")

    # Ajouter la fin du fichier HTML
    f.write("</div></body></html>\n")

# Fermer la connexion à la base de données
conn.close()

print(f"Fichier HTML généré à {html_output}")
