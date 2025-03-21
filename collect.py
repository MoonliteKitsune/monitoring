import sqlite3
import subprocess
import re

# Fonction pour exécuter une sonde et extraire la valeur numérique
def run_sonde(command):
    try:
        # Exécuter la commande et récupérer la sortie
        result = subprocess.check_output(command, shell=True, text=True).strip()
        
        # Extraction de la valeur numérique avec une regex
        match = re.search(r"(\d+\.?\d*)", result)
        if match:
            return float(match.group(1))  # Convertir en float
        else:
            print(f"⚠️ Erreur : Impossible d'extraire une valeur de la sortie '{result}'")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur avec la commande {command}: {e}")
        return None

# Exécution des sondes et récupération des valeurs
cpu = run_sonde("./sondes/cpu_usage.sh")  # Exemple d'une sonde CPU
ram = run_sonde("./sondes/ram_usage.sh")  # Exemple d'une sonde RAM
disk = run_sonde("./sondes/disk_usage.sh")  # Exemple d'une sonde Disque
users = run_sonde("./sondes/users_connected.sh")  # Exemple d'une sonde Utilisateurs

# Connexion à la base de données
conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS monitoring (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage REAL,
    ram_usage REAL,
    disk_usage REAL,
    users_connected INTEGER
)
""")

# Vérification et insertion des données
if cpu is not None and ram is not None and disk is not None and users is not None:
    cursor.execute("INSERT INTO monitoring (cpu_usage, ram_usage, disk_usage, users_connected) VALUES (?, ?, ?, ?)",
                   (cpu, ram, disk, int(users)))
    conn.commit()
    print("✅ Données des sondes enregistrées avec succès !")
else:
    print("⚠️ Erreur : certaines sondes n'ont pas retourné de données valides.")

conn.close()
