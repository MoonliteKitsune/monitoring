import sqlite3
import subprocess
import re
import os
from datetime import datetime

with open("cronlog.txt", "a") as f:
    f.write(f"Script exécuté à : {datetime.datetime.now()}\n")

# Chemin du dossier contenant les sondes
SONDES_DIR = "./sondes/"

# Fonction pour exécuter une sonde et extraire son nom + sa valeur numérique
def run_sonde(command):
    try:
        # Exécuter la commande et récupérer la sortie
        result = subprocess.check_output(command, shell=True, text=True).strip()

        # Extraction du nom de la sonde et de la valeur numérique
        match = re.search(r"(.+?)\s*:\s*(\d+\.?\d*)", result)
        if match:
            sonde = match.group(1).strip()  # Nom de la sonde (texte avant ":")
            valeur = float(match.group(2))  # Valeur numérique
            return sonde, valeur
        else:
            print(f"❌ Erreur : Impossible d'extraire une valeur de la sortie '{result}'")
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur avec la commande {command}: {e}")
        return None, None

# Détection automatique des sondes dans le dossier `sondes/`
sondes = [
    os.path.join(SONDES_DIR, f) for f in os.listdir(SONDES_DIR)
    if os.path.isfile(os.path.join(SONDES_DIR, f)) and os.access(os.path.join(SONDES_DIR, f), os.X_OK)
]

# Connexion à la base de données
conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

# Création de la table sous la forme (date | sonde | valeur)
cursor.execute("""
CREATE TABLE IF NOT EXISTS monitoring (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sonde TEXT,
    valeur REAL
)
""")

# Récupération et insertion des données
for cmd in sondes:
    sonde, valeur = run_sonde(cmd)
    if sonde and valeur is not None:
        cursor.execute("INSERT INTO monitoring (sonde, valeur) VALUES (?, ?)", (sonde, valeur))
        conn.commit()
        print(f"✅ Données de '{sonde}' enregistrées avec succès : {valeur}")
    else:
        print(f"⚠️ Erreur : la sonde '{cmd}' n'a pas retourné de données valides.")

conn.close()
