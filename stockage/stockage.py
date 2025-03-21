import dbm
import json
from datetime import datetime, timedelta

class DataStorage:
    def __init__(self, storage_file="data_storage.db", max_size=99, max_age_days=7):
        """
        Initialise le fichier de stockage dbm avec une taille d'historique définie et un nettoyage des anciennes données.
        
        - storage_file : le fichier de stockage dbm
        - max_size : le nombre maximal d'entrées dans l'historique
        - max_age_days : la durée maximale en jours pendant laquelle les données sont conservées
        """
        self.storage_file = storage_file
        self.max_size = max_size  # Taille maximale de l'historique
        self.max_age_days = max_age_days  # Durée maximale de conservation des données

    def save_data(self, data):
        """Enregistre les données sous forme de clé-valeur dans la base dbm."""
        try:
            with dbm.open(self.storage_file, 'c') as db:
                timestamp = data["timestamp"]
                
                # Nettoyer les anciennes données si nécessaire
                self.cleanup_data(db)
                
                # Stocke les données en JSON sous la clé du timestamp
                db[timestamp] = json.dumps(data)
                print("Données enregistrées avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des données : {e}")

    def cleanup_data(self, db):
        """Nettoie les anciennes données si la taille de la base dépasse la limite ou si les données sont trop anciennes."""
        # Supprimer les données obsolètes par âge
        now = datetime.now()
        keys_to_delete = []
        
        for key in db.keys():
            timestamp_str = key.decode('utf-8')
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            # Supprimer les données plus anciennes que max_age_days
            if now - timestamp > timedelta(days=self.max_age_days):
                keys_to_delete.append(key)

        # Supprimer les données trop anciennes
        for key in keys_to_delete:
            del db[key]
            print(f"Suppression des données obsolètes pour le timestamp : {key.decode('utf-8')}")

        # Supprimer les données si la taille dépasse la limite
        if len(db.keys()) > self.max_size:
            # Trier les clés par date croissante et supprimer les plus anciennes
            sorted_keys = sorted(db.keys(), key=lambda k: datetime.strptime(k.decode('utf-8'), "%Y-%m-%d %H:%M:%S"))
            keys_to_delete = sorted_keys[:len(db) - self.max_size]
            for key in keys_to_delete:
                del db[key]
                print(f"Suppression des anciennes données pour le timestamp : {key.decode('utf-8')}")

    def get_data(self, timestamp):
        """Récupère les données enregistrées pour un timestamp donné."""
        try:
            with dbm.open(self.storage_file, 'r') as db:
                if timestamp in db:
                    return json.loads(db[timestamp].decode())  # Retourne les données sous forme de dictionnaire
                else:
                    print("Aucune donnée trouvée pour ce timestamp.")
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    def list_all_data(self):
        """Liste tous les timestamps et leurs données associées, triées par date."""
        try:
            with dbm.open(self.storage_file, 'r') as db:
                if len(db.keys()) == 0:
                    print("Aucune donnée trouvée.")
                else:
                    print("\nDonnées complètes enregistrées :")
                    # Convertir les clés en une liste de tuples (clé, valeur), puis trier par date
                    sorted_keys = sorted(db.keys(), key=lambda k: datetime.strptime(k.decode('utf-8'), "%Y-%m-%d %H:%M:%S"))
                    
                    # Afficher les données triées
                    for key in sorted_keys:
                        stored_data = json.loads(db[key].decode("utf-8"))
                        print(f"Timestamp: {key.decode('utf-8')}")
                        print(json.dumps(stored_data, indent=4))
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")


    def get_length(self):
        """Retourne le nombre de clés (entrées) dans la base de données."""
        try:
            with dbm.open(self.storage_file, 'r') as db:
                return len(db.keys())  # Retourne le nombre de clés (timestamps)
        except Exception as e:
            print(f"Erreur lors de la récupération de la taille de la base de données : {e}")
            return 0
