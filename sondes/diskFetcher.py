import psutil

disk = psutil.disk_usage('/')
print(f'{{ "%DISK": "{disk.percent}" }}')