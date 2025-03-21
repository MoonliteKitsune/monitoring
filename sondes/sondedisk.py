import psutil

disk=psutil.disk_usage('/').percent
print(f"Utilisation du disque : {disk}")
