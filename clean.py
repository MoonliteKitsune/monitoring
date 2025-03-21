import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

# Suppression des entrées plus vieilles que 7 jours
cursor.execute("DELETE FROM monitoring WHERE timestamp < datetime('now', '-7 days')")

# Sauvegarde et fermeture
conn.commit()
conn.close()

print("🗑️ Anciennes données supprimées.")
