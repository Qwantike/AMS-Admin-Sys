import smtplib
import ssl
import certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config_manager import load_config  # Charger la config depuis config_manager

# Charger la config au début
config = load_config()

# Fonction pour envoyer un e-mail d'alerte
def send_alert_email(subject, message):
    try:
        # Créer un message multipart
        email_message = MIMEMultipart()
        email_message["Subject"] = subject
        email_message["From"] = config['email_sender']
        email_message["To"] = config['email_receiver']
        
        # Contenu du message
        part = MIMEText(message, "plain")
        email_message.attach(part)

        # Solution pour utiliser un certificat sécurisé avec certifi
        context = ssl.create_default_context(cafile=certifi.where())

        # Connexion et envoi de l'email via SMTP sécurisé
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'], context=context) as server:
            print("Connexion établie avec le serveur SMTP")
            server.login(config['email_sender'], config['email_password'])
            print("Authentification réussie")
            server.sendmail(config['email_sender'], config['email_receiver'], email_message.as_string())
            print("Alerte envoyée par e-mail.")
    
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'alerte par e-mail: {e}")
