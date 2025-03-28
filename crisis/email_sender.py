import smtplib
import json

# Charger la configuration du fichier config.json
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Charger la config au début
config = load_config()

# Fonction pour envoyer un e-mail d'alerte
def send_alert_email(subject, message):
    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['email_sender'], config['email_password'])
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(config['email_sender'], config['email_receiver'], email_message)
        print("Alerte envoyée par e-mail.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'alerte par e-mail: {e}")
