import psutil

cpu=psutil.cpu_percent(interval = 1)
nbcpu=psutil.cpu_count()
print(f"Utilisation du cpu : {cpu}")
print(f"Nombre de cpu : {nbcpu}")
