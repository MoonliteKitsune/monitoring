import requests
import sqlite3
from bs4 import BeautifulSoup

# URL de la page web à analyser
url = "https://www.cert.ssi.gouv.fr/"

# Télécharger le contenu de la page
response = requests.get(url)

# Parser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Trouver le premier élément avec la classe "cert-alert"
first = soup.find(class_="items-list")
date = first.find(class_="item-date")
ref = first.find(class_="item-ref")
titre = first.find(class_="item-title")
status = first.find(class_="item-status")
a=date.text.strip()
b=ref.text.strip()
c=titre.text.strip()
d=status.text.strip()

conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

        # Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        ref TEXT,
        titre TEXT,
        status TEXT
)
""")

        # Insérer l'alerte dans la base de données
cursor.execute("INSERT INTO alerte (date, ref, titre, status) VALUES (?, ?, ?, ?)", 
                (a, b, c, d))

conn.commit()
conn.close()

print(" Première alerte enregistrée avec succès !")
print(f" Titre : {c}")
print(f" ref  : {b}")
print(f" status  : {d}")

