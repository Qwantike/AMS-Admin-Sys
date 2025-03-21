import subprocess
import time
import json
from datetime import datetime

scripts = [
    "sondes/diskFetcher.py",
    "sondes/processusFetcher.py",
    "sondes/ramFetcher.py",
    "sondes/usersFetcher.sh",
]

def run_script(script_name):
    try:
        if script_name.endswith(".sh"):
            result = subprocess.run(["bash", script_name], check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(["python3", script_name], check=True, capture_output=True, text=True)

        # Récupérer la sortie du script formaté JSON
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script {script_name}: {e}")
        return None

def gather_data():
    data = {}
    
    # Date & heure en entête
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Ajout dans le json à la clé timestamp
    data["timestamp"] = current_time  
    
    # Exécution des scripts et récupération de leurs sorties
    for script in scripts:
        output = run_script(script)
        
        if output:
            # Vérifie si la sortie est en JSON et l'ajoute au dictionnaire
            try:
                json_data = json.loads(output)
                data.update(json_data)
            except json.JSONDecodeError:
                # Si ce n'est pas du JSON, on l'ajoute avec le nom du fichier 
                data[script] = output
    
    return data

def display_data(data):
    # Affichage des données sous forme de JSON
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    while True:
        data = gather_data()  # Récupère toutes les données des scripts
        display_data(data)  # Affiche les données en JSON
        time.sleep(30)  # Attendre 5 secondes avant de relancer les scripts
