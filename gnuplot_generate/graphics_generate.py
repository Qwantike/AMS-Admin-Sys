import os
import subprocess

GRAPHICS_DIR = "static/graphics"

def get_min_max(dat_file):
    """Lit un fichier .dat et retourne le min/max de la colonne 3 (valeurs numériques), avec marge si nécessaire."""
    values = []
    with open(dat_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:  # Vérification des 3 colonnes
                try:
                    values.append(float(parts[2]))  # Récupération de la valeur numérique (colonne 3)
                except ValueError:
                    continue  # Ignore les lignes incorrectes
    if values:
        ymin, ymax = min(values), max(values)
        if ymin == ymax:  # Si toutes les valeurs sont identiques, ajoute une marge
            ymin -= 1
            ymax += 1
        return ymin, ymax
    return None, None  # Si aucune donnée valide

def prepare_gnuplot_data(data_list):
    """Crée un fichier .dat par métrique avec les données pour Gnuplot."""
    if not os.path.exists(GRAPHICS_DIR):
        os.makedirs(GRAPHICS_DIR)

    metrics = {"%DISK": "DISK", "%RAM": "RAM", "PROCESSUS": "PROCESSUS", "USERS": "USERS"}

    for metric in metrics:
        file_path = os.path.join(GRAPHICS_DIR, f"{metric}.dat")
        
        print(f"Traitement des données pour {metric}...")
        with open(file_path, "w") as f:
            for entry in data_list:
                # Affichage des données avant de les écrire
                value = entry.get(metric)
                timestamp = entry.get("timestamp")
                if value:  # Si la valeur est présente
                    f.write(f"{timestamp} {value}\n")
                else:
                    print(f"Pas de données pour {metric} à {timestamp}")
        print(f"Fichier de données pour {metric} créé.")

    
def generate_graphs():
    """Génère les graphiques avec Gnuplot."""
    metrics = {"%DISK": "%DISK", "%RAM": "%RAM", "PROCESSUS": "PROCESSUS", "USERS": "USERS"}

    for original_metric, clean_metric in metrics.items():
        dat_file = os.path.join(GRAPHICS_DIR, f"{original_metric}.dat")
        png_file = os.path.join(GRAPHICS_DIR, f"{clean_metric}.png")

        # Vérification de l'existence du fichier .dat
        if not os.path.exists(dat_file) or os.stat(dat_file).st_size == 0:
            print(f"⚠️ Aucune donnée pour {clean_metric}, graphique ignoré.")
            continue

        # Calcul min/max en Python
        ymin, ymax = get_min_max(dat_file)
        if ymin is None or ymax is None:
            print(f"⚠️ Pas de données valides pour {clean_metric}, graphique ignoré.")
            continue

        # Ajout d'une marge de 10% pour l'affichage
        y_margin = (ymax - ymin) * 0.1
        y_range = f"[{ymin - y_margin}:{ymax + y_margin}]"

        gnuplot_script = f"""
        set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
        set output '{png_file}'
        set title 'Évolution de {clean_metric}' font 'Verdana,12'

        # Configuration des axes
        set xdata time
        set timefmt "%Y-%m-%d %H:%M:%S"
        set format x "%d/%m\\n%H:%M"
        set xlabel 'Temps' font 'Verdana,10'
        set ylabel '{clean_metric}' font 'Verdana,10'
        set yrange {y_range}

        # Séparateur de données
        set datafile separator " "

        # Amélioration affichage X
        set xtics rotate by -45
        set autoscale xfixmin
        set autoscale xfixmax

        # Grille et style
        set grid
        set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 0.5

        # Tracé des valeurs
        plot '{dat_file}' using 1:3 with lines ls 1 title '{clean_metric}'
        """

        script_path = os.path.join(GRAPHICS_DIR, f"{clean_metric}.gnu")
        try:
            with open(script_path, "w") as f:
                f.write(gnuplot_script)

            subprocess.run(["gnuplot", script_path], check=True)
            print(f"✅ Graphique généré pour {clean_metric} avec succès!")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'exécution de Gnuplot pour {clean_metric} : {e}")
        except FileNotFoundError:
            print(f"❌ Gnuplot n'est pas installé ou non trouvé dans le PATH.")
        except Exception as e:
            print(f"❌ Erreur lors de la génération du graphique pour {clean_metric} : {e}")

    print("🎉 Tous les graphiques ont été générés avec succès !")