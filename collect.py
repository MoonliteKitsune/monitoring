import sqlite3
import subprocess
import re

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
        print(f"Erreur avec la commande {command}: {e}")
        return None, None

# Exécution des sondes et récupération des valeurs
sondes = [
    "./sondes/sondecpu.py",
    "./sondes/sonderam.py",
    "./sondes/sondedisk.py",
    "./sondes/sondeuser.sh",
    "./sondes/sondeprocess.sh"
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
        print(f"Données de '{sonde}' enregistrées avec succès : {valeur}")
    else:
        print(f" Erreur : la sonde '{cmd}' n'a pas retourné de données valides.")

conn.close()
