#!/usr/bin/env python3

import psutil

ram=psutil.virtual_memory().percent
print(f"Pourcentage_de_ram: {ram}")
