import requests
import re
from datetime import datetime
from stockage.stockage import DataStorage

class CertParser:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.url = "https://www.cert.ssi.gouv.fr/"

    def get_last_alert(self):
        """Récupère la dernière alerte CERT sur le site web sans utiliser BeautifulSoup."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Vérifie si la requête a réussi (code 200)

            # Utilisation d'expressions régulières pour extraire les informations
            html_content = response.text

            # Exemple d'expression régulière pour trouver un lien d'alerte
            # Ici, on suppose que l'alerte est dans un <a href="...">titre</a>
            alert_pattern = r'<a href="(/.*?\.html)"[^>]*>(.*?)</a>'
            
            # Recherche des correspondances dans le HTML
            matches = re.findall(alert_pattern, html_content)

            if matches:
                # On prend la première alerte trouvée (supposée être la dernière)
                alert_url = matches[0][0]  # L'URL relative de l'alerte
                alert_title = matches[0][1]  # Le titre de l'alerte
                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Construction de l'URL complète
                full_alert_url = f"https://www.cert.ssi.gouv.fr{alert_url}"

                # Enregistrer l'alerte dans le moteur de stockage
                alert_data = {
                    "timestamp": alert_time,
                    "title": alert_title,
                    "url": full_alert_url
                }

                self.storage.save_data(alert_data)
                print(f"Dernière alerte CERT enregistrée : {alert_title}")

            else:
                print("Aucune alerte trouvée sur le site CERT.")

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de la page CERT : {e}")

# Fonction principale pour exécuter le parseur
def main():
    storage = DataStorage()  # Instance de la classe DataStorage
    parser = CertParser(storage)

    # Récupérer la dernière alerte CERT et la stocker
    parser.get_last_alert()

if __name__ == "__main__":
    main()
