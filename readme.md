Para ejecutar el programa en cada encendido se debe tener el siguiente archivo:

~/.config/autostart/autorun.desktop

[Desktop Entry]
Type=Application
Name=AutoRun Visible
Exec=lxterminal -e bash /home/pi/SIM7600X-4G-HAT-Demo/Raspberry/python/sim_sms_project/run_autorun.sh
Terminal=true
StartupNotify=false
