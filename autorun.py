import subprocess
import pyautogui
import time

#subprocess.Popen(['lxterminal'])

# Esperar y hacer clic
#time.sleep(10)
#pyautogui.moveTo(400, 300)
#pyautogui.doubleClick()
#pyautogui.click()
#pyautogui.write('terminal', interval=0.1)
#pyautogui.press('enter')

# Abrir una aplicacion grafica, como el navegador Chromium
subprocess.Popen(['bash','./run_main.sh'])
