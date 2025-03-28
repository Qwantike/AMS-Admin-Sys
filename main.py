import time
from sondes.controller import gather_data
from stockage.stockage import DataStorage
from stockage.alert_storage import AlertStorage  
from parser.cert_parser import CertParser  
from crisis.crisis_check import check_crisis_conditions
from config.config_manager import load_config
from config.config_manager import load_config  

import json

def main():
    storage = DataStorage()
    alert_storage = AlertStorage()
    parser = CertParser()

    # Récupérer les données des sondes et les stocker
    data = gather_data()
    storage.save_data(data) #sauvegarder les données en json
    config = load_config()  # Charger la configuration
    check_crisis_conditions(data, config)  # Vérifier les crises avec les données

    # Récupérer la dernière alerte CERT et la stocker si elle est nouvelle
    alert_json = parser.get_last_alert()
    if alert_json:
        alert = json.loads(alert_json)
        alert_storage.save_alert(alert)

    # (Optionnel) Ajouter une ligne dans un log pour voir si tout fonctionne
    with open("cron_log.txt", "a") as log:
        log.write(f"Exécution à {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    main()
