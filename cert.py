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

    # Trouver toutes les alertes avec la classe "cert-alert"
    alerts = soup.find_all(class_="cert-alert")

    if alerts:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect("monitoring.db")
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            etat TEXT,
            titre TEXT,
            lien TEXT
        )
        """)

        for alert in alerts:
            alert_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date actuelle
            
            # Récupérer le titre de l'alerte (le texte principal)
            alert_title = alert.text.strip()

            # Récupérer l'état de l'alerte (ex: "Critique", "Alerte", etc.)
            alert_state = alert.find("span") or alert.find("strong")  # Essayons de trouver l'état
            alert_state = alert_state.text.strip() if alert_state else "Inconnu"

            # Récupérer le lien de l’alerte
            alert_link = alert.find("a")["href"] if alert.find("a") else "Aucun lien"

            # Insérer l'alerte dans la base de données
            cursor.execute("INSERT INTO alerte (date, etat, titre, lien) VALUES (?, ?, ?, ?)", 
                           (alert_date, alert_state, alert_title, alert_link))

        conn.commit()
        conn.close()

        print("✅ Toutes les alertes ont été enregistrées avec succès !")
    else:
        print("❌ Aucune alerte trouvée avec la classe 'cert-alert'.")
else:
    print(f"❌ Erreur lors du chargement de la page : {response.status_code}")
