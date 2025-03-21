import time
from sondes.controller import gather_data
from stockage.stockage import DataStorage
from stockage.alert_storage import AlertStorage  
from parser.cert_parser import CertParser  # Assure-toi d'importer la classe CertParser
import json

def main():
    storage = DataStorage()
    alert_storage = AlertStorage()  # Instance du stockage des alertes
    parser = CertParser()  # Instance du parser pour récupérer l'alerte
    start_time = time.time()  # Enregistre l'heure de début

    while True:
        # Récupérer les données des sondes et les stocker
        data = gather_data()
        storage.save_data(data)

        # Récupérer la dernière alerte CERT et la stocker si elle est nouvelle
        alert_json = parser.get_last_alert()
        if alert_json:
            alert = json.loads(alert_json)  # Convertir le JSON en dictionnaire
            alert_storage.save_alert(alert)  # Enregistrer l'alerte

        elapsed_time = time.time() - start_time  # Temps écoulé

        if elapsed_time >= 60:  # 1 minute (60 secondes)
            print("\nDonnées stockées après 1 minute :")
            storage.list_all_data()  # Affiche toutes les données enregistrées
            print(storage.get_length())
            break  # Arrête la boucle après affichage

        time.sleep(1)  # Rafraîchit toutes les 1 secondes

if __name__ == "__main__":
    main()
