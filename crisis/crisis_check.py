import json
from crisis.email_sender import send_alert_email

# Fonction pour vérifier les conditions de crise en utilisant les données des sondes
def check_crisis_conditions(data, config):
    # Vérifier l'utilisation du disque
    disk_usage = float(data.get("%DISK", 0))  # %DISK retourne un nombre sous forme de chaîne, donc on le convertit en float
    if disk_usage > config['disk_usage_threshold']:
        message = f"ALERTE: L'utilisation du disque a dépassé {config['disk_usage_threshold']}%. Actuellement: {disk_usage}%."
        send_alert_email("Crise : Utilisation du disque", message)

    # Vérifier le nombre de processus en cours
    process_count = int(data.get("PROCESSUS", 0))  # PROCESSUS est un entier
    if process_count > config['process_count_threshold']:
        message = f"ALERTE: Le nombre de processus a dépassé {config['process_count_threshold']}. Actuellement: {process_count} processus."
        send_alert_email("Crise : Nombre de processus", message)

    # Vérifier le nombre d'utilisateurs connectés
    user_count = int(data.get("USERS", 0))  # USERS est aussi un entier
    if user_count > config['user_count_threshold']:
        message = f"ALERTE: Le nombre d'utilisateurs connectés a dépassé {config['user_count_threshold']}. Actuellement: {user_count} utilisateurs."
        send_alert_email("Crise : Nombre d'utilisateurs", message)

    # Vérifier l'utilisation de la RAM
    ram_usage = float(data.get("%RAM", 0))  # %RAM est une valeur en pourcentage, donc il faut la traiter comme un float
    if ram_usage > config['ram_usage_threshold']:
        message = f"ALERTE: L'utilisation de la RAM a dépassé {config['ram_usage_threshold']}%. Actuellement: {ram_usage}%."
        send_alert_email("Crise : Utilisation de la RAM", message)
