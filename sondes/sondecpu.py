#!/usr/bin/env python3

import psutil

cpu=psutil.cpu_percent(interval = 1)
print(f"Utilisation du cpu : {cpu}")

