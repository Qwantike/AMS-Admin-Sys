import dbm
import json
from datetime import datetime, timedelta

class AlertStorage:
    def __init__(self, storage_file="alert_storage.db", max_size=99, max_age_days=7):
        self.storage_file = storage_file
        self.max_size = max_size
        self.max_age_days = max_age_days

    def save_alert(self, alert):
        """Enregistre une alerte dans le fichier dbm si elle n'est pas déjà présente."""
        try:
            with dbm.open(self.storage_file, 'c') as db:
                alert_id = alert["alert_id"]

                # Vérifier si l'alerte existe déjà
                if alert_id in db:
                    print(f"L'alerte {alert_id} est déjà enregistrée.")
                    return  # L'alerte existe déjà, ne rien faire

                # Nettoyer les alertes anciennes si nécessaire
                self.cleanup_alerts(db)

                # Enregistrer la nouvelle alerte
                db[alert_id] = json.dumps(alert)
                print(f"Alerte {alert_id} enregistrée avec succès.")

        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'alerte : {e}")
    
    def cleanup_alerts(self, db):
        """Nettoie les anciennes alertes si nécessaire."""
        now = datetime.now()
        keys_to_delete = []
        
        for key in db.keys():
            alert_id = key.decode('utf-8')
            alert = json.loads(db[key].decode('utf-8'))
            alert_timestamp = datetime.strptime(alert["timestamp"], "%Y-%m-%d %H:%M:%S")
            # Supprimer les alertes plus anciennes que max_age_days
            if now - alert_timestamp > timedelta(days=self.max_age_days):
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del db[key]
            print(f"Suppression de l'alerte pour le ID : {key.decode('utf-8')}")

    def get_alert(self, alert_id):
        """Récupère une alerte par son ID."""
        try:
            with dbm.open(self.storage_file, 'r') as db:
                if alert_id in db:
                    return json.loads(db[alert_id].decode())  # Retourne l'alerte sous forme de dictionnaire
                else:
                    print("Aucune alerte trouvée pour cet ID.")
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'alerte : {e}")
            return None
