# sim7600.py

import serial
import time
import RPi.GPIO as GPIO
from config import SERIAL_PORT, BAUD_RATE, POWER_KEY_GPIO
import threading
serial_lock = threading.Lock()

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
ser.flushInput()

def send_at(command, back, timeout):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        rec_buff = ser.read(ser.inWaiting()).decode()
        if back not in rec_buff:
            print(f"Error en: {command}, respuesta: {rec_buff}")
            return False
        return True
    return False

def init_modem():
    print("Encendiendo SIM7600...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_KEY_GPIO, GPIO.OUT)
    GPIO.output(POWER_KEY_GPIO, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(POWER_KEY_GPIO, GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print("Modem listo")

def send_sms(phone_number, text_message):
    with serial_lock:  # Evita conflictos si varios hilos usan el modem a la vez
        print("Enviando SMS...")
        if not send_at("AT+CMGF=1", "OK", 1): return
        if not send_at(f'AT+CMGS="{phone_number}"', ">", 2): return
        ser.write(text_message.encode())
        ser.write(b'\x1A')  # Ctrl+Z
        if send_at("", "OK", 20):
            print("SMS enviado correctamente")
        else:
            print("Fallo en envio de SMS")

def cleanup():
    GPIO.cleanup()
    ser.close()
