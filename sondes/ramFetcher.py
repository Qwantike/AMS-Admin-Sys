import psutil

memory = psutil.virtual_memory()
print(f'{{ "%RAM": "{memory.percent}" }}')
