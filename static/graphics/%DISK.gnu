
        set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
        set output 'static/graphics/%DISK.png'
        set title 'Évolution de %DISK' font 'Verdana,12'

        # Configuration des axes
        set xdata time
        set timefmt "%Y-%m-%d %H:%M:%S"
        set format x "%d/%m\n%H:%M"
        set xlabel 'Temps' font 'Verdana,10'
        set ylabel '%DISK' font 'Verdana,10'
        set yrange [32.67:33.03]

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
        plot 'static/graphics/%DISK.dat' using 1:3 with lines ls 1 title '%DISK'
        