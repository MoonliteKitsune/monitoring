from flask import Flask

app = Flask(__name__)

@app.route('/')
def accueil():
    return "Hello depuis Flask sur ma VM 🚀"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
