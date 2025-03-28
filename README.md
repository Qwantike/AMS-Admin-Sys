installation de python : sudo apt install python3-pip
installation de psutil : sudo apt install python3-psutil

[Wikipedia - DBM](https://fr.wikipedia.org/wiki/Dbm)

Controller.py : réccupère dynamiquement les fichiers finissant par Fetcher.py/sh pour pouvoir ajouter des sondes sans avoir à modifier le code pour leur prise en compte.
Le stockage est formaté en JSON et est stocké en local avec dbm

##cron : 
crontab -e
utiliser pwd pour connaitre le chemin absolu du fichier
* * * * * /usr/bin/python3 /chemin/vers/main.py
Pour arrêter : crontab -r (stop tous les cron)
ou crontab -e  -> supprimer ligne

sur mon pc : 

* * * * * /usr/bin/python3 /home/paul/Documents/Licence/L2-INFO/S4/AMS_System/main.py

Ajouter un fichier de log (créer automatiquement si pas présent)

* * * * * /usr/bin/python3 /home/paul/Documents/Licence/L2-INFO/S4/AMS_System/main.py >> /home/paul/cron_output.log 2>&1


pip install python-dotenv

/home/paul/AMS-Admin-Sys/main.py