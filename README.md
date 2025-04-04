# PROJET ADMIN SYS 

## Objectif 

Créer une interface pour pouvoir connaître et suivre l'état des machines d'un parc et être alerter par mail en cas de situation de crise (ex : disque presque remplit) via un serveur LINUX. 

## Installation 

installation de python : sudo apt install python3-pip  
installation de psutil : sudo apt install python3-psutil  
installation de flask : sudo apt install python3-flask  
installation de gnuplot : sudo apt install python3-gnuplot  
installation de dotenv : sudo apt install python-dotenv  


### Ajouter main.py à cron

Cron permet de lancer des scripts automatiquement sans bloquer l'interface du serveur. Le script qui sonde l'état des machines est dont lancé toutes les 5 minutes :  
`crontab -e`  
Rajouter la ligne :  
`*/5 * * * * /usr/bin/python3 /chemin/vers/main.py`

### Lancer le serveur

Lancer le fichier `app.py` avec la commande `python3 app.py`  
(possibilité de le mettre dans cron également).

## Description des scripts

### Config 

#### config_manager

Permet de charger les valeurs du .env pour les variables nécessaires à l'envoie de mail.  
Permet également de modifier les seuils critiques des valeurs à surveiller.  

### Crisis 

#### crisis_check 

Compare les valeurs récupérées sur les machines avec le seuil critique mis en place, s'il est dépassé, envoie un mail d'alerte.  

#### email_sender

Envoie un mail avec la valeur critique qui été dépassée, précise la donnée, la valeur actuelle et la valeur limite.  

### Gnuplot_generate

#### graphics_generate

1. Fonction pour récupérer les valeurs min et max des timestamp pour organiser l'axe y des graphiques.  

2. Fonction qui récupère toutes les données (format JSON) puis les transforme en différents tableaux de données pour chaque donnée à surveiller (users, %ram, %disk ...)  

3. Fonction qui créer un script .gnu pour générer les différents graphes nécessaires.  

### Parser

#### cert_parser

Récupère la dernière alerte sur le site du [CERT](https://www.cert.ssi.gouv.fr) et les stock dans une base de donnée en JSON.  

### Sondes

Récupère différentes informations lié à l'état de la machine.  

#### diskFetcher

Récupère l'utilisation du disque en %.  

#### processusFetcher

Récupère le nombre de processus en cours.  

#### ramFetcher

Récupère le % de RAM en cours d'utilisation.  

#### usersFetcher

Récupère le nombre d'utilisateurs connecté actuellement.  

#### controller

S'occupe de centraliser toutes les informations et les stock en JSON avec comme clé le timestamp du sondage.  

### Static/Graphics

#### .dat

Pour chaque attribut, fichier avec en colonne 1, 2 le timestamp (jour heure) et en colonne 3 la valeur de l'attribut sondé.  

#### .gnu

Scripts générés dynamiquement pour créer un graphique pour chaque attribut.  

#### .png

Graphiques générés par le script gnuplot  
 
### Stockage

#### alert_storage

Stock les alertes du CERT, l'alerte parsé n'est ajouté que si elle est différente de la dernière (nouvelle alerte).  

#### stockage

Stock en JSON les valeurs récupérées par les sondes avec comme clé le timestamp.  

Suppression automatique des valeurs si elles sont présente depuis plus d'une semaine (modifiable) et des dernières en cas de dépassement de 100 jeu de données enregistrés (modifiable).  

Les données sont enregistré avec DBM dans des fichiers .db au format JSON.  

### Template

#### index.html

Gère l'affichage de la page web (html, css).  

### .env

Contient les variables nécessaire à la connexion au serveur SMTP.  

### main

Appel les fonctions pour récupérer les données (sondes et alerte CERT), les stock, vérifie si une situation de crise est rencontrée (ce qui génère un envoi de mail).
Permet également de formater les données pour gnuplot, générer les scripts gnuplot puis les graphiques.   

### app

Lance un serveur flask sur le port 5000  