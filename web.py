from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def ouvrir_fichier_html():
    # Renvoie le fichier 'resultat.html' situé dans le même dossier que web.py
    return send_file('graphiques_sondes.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
