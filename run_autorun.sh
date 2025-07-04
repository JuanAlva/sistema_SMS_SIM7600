#!/bin/bash

# Configurar entorno grafico si es necesario
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority

# Activar entorno virtual si lo usas
cd /home/pi/SIM7600X-4G-HAT-Demo/Raspberry/python/sim_sms_project
source entorno_autorun/bin/activate

# Ejecutar el script Python con ruta correcta
python autorun.py

echo "Script ejecutando. Presiona ENTER para cerrar..."
read
