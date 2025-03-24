import sqlite3
import subprocess
import re
import os
import datetime

# Chemin absolu du répertoire contenant le script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SONDES_DIR = os.path.join(SCRIPT_DIR, "sondes")

# Vérifie si le répertoire existe
if not os.path.exists(SONDES_DIR):
    print(f"Le répertoire {SONDES_DIR} n'existe pas.")
else:
    sondes = [
        os.path.join(SONDES_DIR, f) for f in os.listdir(SONDES_DIR)
        if os.path.isfile(os.path.join(SONDES_DIR, f)) and os.access(os.path.join(SONDES_DIR, f), os.X_OK)
    ]

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
            print(f" Erreur : Impossible d'extraire une valeur de la sortie '{result}'")
            return None, None
    except subprocess.CalledProcessError as e:
        print(f" Erreur avec la commande {command}: {e}")
        return None, None

# Détection automatique des sondes dans le dossier `sondes/`
sondes = [
    os.path.join(SONDES_DIR, f) for f in os.listdir(SONDES_DIR)
    if os.path.isfile(os.path.join(SONDES_DIR, f)) and os.access(os.path.join(SONDES_DIR, f), os.X_OK)
]

# Connexion à la base de données
conn = sqlite3.connect("/home/elprimooooo/ams/monitoring/monitoring.db")
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
        try:
            cursor.execute("INSERT INTO monitoring (sonde, valeur) VALUES (?, ?)", (sonde, valeur))
            conn.commit()
            print(f" Données de '{sonde}' enregistrées avec succès : {valeur}")
        except Exception as e:
            print(f" Erreur lors de l'insertion dans la base de données : {e}")
    else:
        print(f" Erreur : la sonde '{cmd}' n'a pas retourné de données valides.")

conn.close()
