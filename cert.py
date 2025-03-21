import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

# URL de la page web à analyser
url = "https://www.cert.ssi.gouv.fr/"

# Télécharger le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver le premier élément avec la classe "cert-alert"
    first_alert = soup.find(class_="cert-alert")

    if first_alert:
        alert_text = first_alert.text.strip()
        alert_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date actuelle

        # Connexion à la base de données SQLite
        conn = sqlite3.connect("monitoring.db")
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            alerte TEXT
        )
        """)

        # Insérer l'alerte dans la base de données
        cursor.execute("INSERT INTO alerte (date, alerte) VALUES (?, ?)", (alert_date, alert_text))
        conn.commit()
        conn.close()

        print(f"✅ Alerte enregistrée : {alert_text}")
    else:
        print("❌ Aucune alerte trouvée avec la classe 'cert-alert'.")
else:
    print(f"❌ Erreur lors du chargement de la page : {response.status_code}")
