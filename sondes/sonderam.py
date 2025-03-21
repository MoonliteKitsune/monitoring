#!/usr/bin/env python3

import psutil

ram=psutil.virtual_memory().percent
print(f"Pourcentage de ram : {ram}")
