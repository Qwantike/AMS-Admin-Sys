
        set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
        set output 'static/graphics/USERS.png'
        set title 'Évolution de USERS' font 'Verdana,12'

        # Configuration des axes
        set xdata time
        set timefmt "%Y-%m-%d %H:%M:%S"
        set format x "%d/%m\n%H:%M"
        set xlabel 'Temps' font 'Verdana,10'
        set ylabel 'USERS' font 'Verdana,10'
        set yrange [-0.2:2.2]

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
        plot 'static/graphics/USERS.dat' using 1:3 with lines ls 1 title 'USERS'
        