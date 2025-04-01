#!/bin/bash
nbprocess=$(ps -e --no-headers | wc -l)
echo "Nombre_de_processus_en_cours: $nbprocess"
