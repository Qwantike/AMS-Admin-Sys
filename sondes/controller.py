import subprocess
import json
import os
from datetime import datetime

SONDES_DIR = "sondes"  # Dossier contenant les sondes

def get_sondes():
    """Récupère dynamiquement la liste des scripts de sondes disponibles dans le dossier, avec un suffixe spécifique."""
    sondes = []
    for file in os.listdir(SONDES_DIR):
        # Vérifie que le fichier se termine par Fetcher.py ou Fetcher.sh
        if (file.endswith("Fetcher.py") or file.endswith("Fetcher.sh")):
            sondes.append(os.path.join(SONDES_DIR, file))  # Chemin complet du script
    return sondes

def run_script(script_name):
    try:
        if script_name.endswith(".sh"):
            result = subprocess.run(["bash", script_name], check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(["python3", script_name], check=True, capture_output=True, text=True)

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script {script_name}: {e}")
        return None

def gather_data():
    """Récupère les données de toutes les sondes disponibles."""
    data = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    sondes = get_sondes()
    for script in sondes:
        output = run_script(script)
        if output:
            try:
                json_data = json.loads(output)
                data.update(json_data)
            except json.JSONDecodeError:
                data[script] = output
    
    return data
