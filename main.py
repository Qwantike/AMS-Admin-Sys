import time
from sondes.controller import gather_data
from stockage.stockage import DataStorage

def main():
    storage = DataStorage()
    start_time = time.time()  # Enregistre l'heure de début

    while True:
        data = gather_data()
        storage.save_data(data)

        elapsed_time = time.time() - start_time  # Temps écoulé

        if elapsed_time >= 120:  # 2 minutes (120 secondes)
            print("\nDonnées stockées après 1 minute :")
            storage.list_all_data()  # Affiche toutes les données enregistrées
            print(storage.get_length())
            break  # Arrête la boucle après affichage

        time.sleep(1)  # Rafraîchit toutes les 1 secondes

if __name__ == "__main__":
    main()
