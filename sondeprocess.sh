#!/bin/bash
nbprocess=$(ps -e --no-headers | wc -l)
echo "Nombre de processus en cours  : $nbprocess"