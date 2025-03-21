import psutil

process_count = len(psutil.pids())
print(f'{{ "PROCESSUS": "{process_count}" }}')