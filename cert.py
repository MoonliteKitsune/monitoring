import requests
from bs4 import BeautifulSoup

# URL de la page des alertes CERT-FR
url = "https://www.cert.ssi.gouv.fr/"

# Télécharger le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver la première alerte (elle est généralement dans une balise <article>)
    first_alert = soup.find("article")

    if first_alert:
        # Extraire le titre de l'alerte
        alert_title = first_alert.find("h2").text.strip()

        # Extraire le lien de l'alerte
        alert_link = first_alert.find("a")["href"]
        alert_url = f"https://www.cert.ssi.gouv.fr{alert_link}"

        print(f"🚨 Première alerte : {alert_title}")
        print(f"🔗 Lien : {alert_url}")
    else:
        print("❌ Aucune alerte trouvée.")
else:
    print(f"❌ Erreur lors du chargement de la page : {response.status_code}")
