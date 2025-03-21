from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

class CertParser:
    def __init__(self):
        self.url = "https://www.cert.ssi.gouv.fr/"

    def get_last_alert(self):
        """Récupère la dernière alerte CERT et la renvoie sous forme de JSON."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Trouver toutes les alertes
            alerts = soup.find_all("div", class_="item cert-alert open")

            if alerts:
                first_alert = alerts[0]

                # Extraction des données
                alert_date = first_alert.find("span", class_="item-date").text.strip()
                alert_ref = first_alert.find("div", class_="item-ref").a.text.strip()
                alert_title = first_alert.find("div", class_="item-title").a.text.strip()
                alert_url = first_alert.find("div", class_="item-title").a["href"].strip()

                # Convertir la date
                date_obj = datetime.strptime(alert_date, "%d %B %Y")
                alert_time = date_obj.strftime("%Y-%m-%d")

                # URL complète
                full_alert_url = f"https://www.cert.ssi.gouv.fr{alert_url}"

                # Nouvelle alerte sous forme de dictionnaire
                new_alert = {
                    "alert_id": alert_ref,
                    "timestamp": alert_time,
                    "title": alert_title,
                    "url": full_alert_url
                }

                return json.dumps(new_alert)  # Retourner l'alerte sous forme de JSON

            else:
                print("⚠️ Aucune alerte trouvée.")
                return None

        except requests.RequestException as e:
            print(f"Erreur de récupération : {e}")
            return None

# Exécution
def main():
    parser = CertParser()
    alert_json = parser.get_last_alert()
    
    if alert_json:
        print(f"Alerte CERT récupérée : {alert_json}")
        # Si tu souhaites enregistrer dans le stockage, fais-le ici :
        # storage = AlertStorage()
        # storage.save_alert(json.loads(alert_json))

if __name__ == "__main__":
    main()
