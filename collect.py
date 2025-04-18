import sqlite3
import subprocess
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

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


def envoyer_alerte(sujet, sonde, valeur, seuil):
    # Charger le template depuis un fichier
    template_path = "template.txt"
    with open(template_path, "r") as f:
        template_content = f.read()

    # Créer un objet Template et remplacer les variables
    template = Template(template_content)
    message = template.substitute(sujet=sujet, sonde=sonde, seuil=seuil, valeur=valeur)

    # Informations sur l'email
    sender_email = "nathan.bartier@alumni.univ-avignon.fr"
    receiver_email = "nathan.bartier@alumni.univ-avignon.fr"
    smtp_server = "partage.univ-avignon.fr"
    smtp_port = 465
    username = "nathan.bartier@alumni.univ-avignon.fr"
    password = os.getenv("SMTP_PASSWORD")  # Utiliser une variable d'environnement pour la sécurité

    # Préparer le message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = sujet
    msg.attach(MIMEText(message, "plain"))

    try:
        # Connexion au serveur SMTP et envoi du message
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
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
            
            if sonde == "Utilisation_du_disque" and valeur >= 10:
                # Définir un seuil pour l'alerte de disque
                seuil = 10
                envoyer_alerte("Alerte Disque Plein", sonde, valeur, seuil)
            elif sonde == "Pourcentage_de_ram" and valeur >= 1:
                # Définir un seuil pour l'alerte de RAM
                seuil = 1
                envoyer_alerte("Alerte RAM Saturée", sonde, valeur, seuil)
            
        except Exception as e:
            print(f" Erreur lors de l'insertion dans la base de données : {e}")
    else:
        print(f" Erreur : la sonde '{cmd}' n'a pas retourné de données valides.")
        
conn.close()
