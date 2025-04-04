from flask import Flask

app = Flask(__name__)

@app.route('/')
def accueil():
    return "<h1>Bienvenue sur mon serveur Flask dans la VM ! 🎉</h1><p>Ça fonctionne !</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
