import requests
from bs4 import BeautifulSoup
import sqlite3

# URL des alertes CERT
CERT_URL = "https://www.cert.ssi.gouv.fr/"

try:
    # Récupération de la page web
    response = requests.get(CERT_URL, timeout=10)
    response.raise_for_status()  # Vérifie si l'URL est accessible
except requests.exceptions.RequestException as e:
    print(f"❌ Erreur lors de la récupération de la page CERT : {e}")
    exit(1)

# Analyse du HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extraction du dernier titre d'alerte
latest_alert = soup.find("a", class_="news-title")

if latest_alert:
    latest_alert_text = latest_alert.text.strip()
else:
    print("❌ Erreur : Impossible de trouver une alerte CERT sur la page.")
    exit(1)

# Connexion à la base de données
conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    alert TEXT
)
""")

# Insertion de l'alerte dans la base
cursor.execute("INSERT INTO alerts (alert) VALUES (?)", (latest_alert_text,))

# Sauvegarde et fermeture
conn.commit()
conn.close()

print(f"✅ Nouvelle alerte CERT enregistrée : {latest_alert_text}")
