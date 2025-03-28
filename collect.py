import sqlite3
import subprocess
import re
import os
import smtplib
from email.mime.text import MIMEText

# Chemin absolu du répertoire contenant le script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SONDES_DIR = os.path.join(SCRIPT_DIR, "sondes")


if not os.path.exists(SONDES_DIR):
    print(f"Le répertoire {SONDES_DIR} n'existe pas.")
else:
    sondes = [
        os.path.join(SONDES_DIR, f) for f in os.listdir(SONDES_DIR)
        if os.path.isfile(os.path.join(SONDES_DIR, f)) and os.access(os.path.join(SONDES_DIR, f), os.X_OK)
    ]

def run_sonde(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        
        if ':' in result:
            parts = result.split(':', 1)  
            sonde = parts[0].strip()  
            sonde = os.path.splitext(sonde)[0] 
            try:
                valeur = float(parts[1].strip())  
                return sonde, valeur
            except ValueError:
                print(f"Erreur : Impossible de convertir '{parts[1].strip()}' en nombre.")
                return None, None
        else:
            print(f"Erreur : Format inattendu dans la sortie '{result}'")
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"Erreur avec la commande {command}: {e}")
        return None, None

def envoyer_alerte(sujet, message):
    sender = "alerte@monitoring.com"
    receiver = "nathan.bartier@alumni.univ-avignon.fr"
    msg = MIMEText(message)
    msg["Subject"] = sujet
    msg["From"] = sender
    msg["To"] = receiver
    
    try:
        with smtplib.SMTP("localhost") as server:
            server.sendmail(sender, [receiver], msg.as_string())
        print("Alerte envoyée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'alerte : {e}")

sondes = [
    os.path.join(SONDES_DIR, f) for f in os.listdir(SONDES_DIR)
    if os.path.isfile(os.path.join(SONDES_DIR, f)) and os.access(os.path.join(SONDES_DIR, f), os.X_OK)
]

conn = sqlite3.connect("/home/elprimooooo/ams/monitoring/monitoring.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS monitoring (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sonde TEXT,
    valeur REAL
)
""")

for cmd in sondes:
    sonde, valeur = run_sonde(cmd)
    if sonde and valeur is not None:
        try:
            cursor.execute("INSERT INTO monitoring (sonde, valeur) VALUES (?, ?)", (sonde, valeur))
            conn.commit()
            print(f" Données de '{sonde}' enregistrées avec succès : {valeur}")
            
            if sonde.lower() == "sondedisk" and valeur >= 100:
                envoyer_alerte("Alerte Disque Plein", f"Le disque dur est plein à {valeur}%. Veuillez libérer de l'espace.")
            elif sonde.lower() == "sonderam" and valeur >= 100:
                envoyer_alerte("Alerte RAM Saturée", f"La RAM est utilisée à {valeur}%. Veuillez vérifier les processus en cours.")
            
        except Exception as e:
            print(f" Erreur lors de l'insertion dans la base de données : {e}")
    else:
        print(f" Erreur : la sonde '{cmd}' n'a pas retourné de données valides.")

conn.close()
