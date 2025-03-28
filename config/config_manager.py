import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Charge la configuration depuis un fichier JSON."""
    if not os.path.exists(CONFIG_FILE):
        return {
            "disk_usage_threshold": 90,  # Seuil critique pour l'utilisation du disque (%)
            "ram_usage_threshold": 80,   # Seuil critique pour l'utilisation de la RAM (%)
            "process_count_threshold": 200,  # Nombre max de processus
            "user_count_threshold": 0,  # Nombre max d'utilisateurs connectés
            "max_history_entries": 100,  # Nombre max de données stockées
            "history_retention_days": 7,  # Nombre de jours de rétention des données
            "smtp_server": os.getenv("SMTP_SERVER", "partage.univ-avignon.fr"),  
            "smtp_port": int(os.getenv("SMTP_PORT", 465)),
            "email_sender": os.getenv("EMAIL_SENDER", "uapv2401459@etud.univ-avignon.fr"),
            "email_receiver": os.getenv("EMAIL_RECEIVER", "paul.moinereau@alumni.univ-avignon.fr"),
            "email_password": os.getenv("EMAIL_PASSWORD", ""),  # Stocké en .env
            "email_subject": "Alerte Système",
        }
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    """Enregistre la configuration dans un fichier JSON."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
