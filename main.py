#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py

import sim7600
import mqtt_client
import threading
import time

import unicodedata
import re

def limpiar_mensaje(texto):
	# Normaliza caracteres acentuados a su forma basica
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

    # Opcional: reemplaza guiones largos y caracteres especiales
    texto = texto.replace("—", "-").replace("“", "\"").replace("”", "\"")

    # Elimina caracteres no imprimibles
    texto = re.sub(r'[^\x20-\x7E]', '', texto)

    return texto

# Divide el mensaje en partes de hasta 153 caracteres
def split_message(mensaje, max_length=153):
    return [mensaje[i:i+max_length] for i in range(0, len(mensaje), max_length)]

def sms_worker(sms_queue):
    while True:
        sms_data = sms_queue.get()
        if sms_data is None:
            break
    
        number = sms_data["number"]
        label = sms_data["label"]
        mensaje = sms_data["mensaje"]

        # Limpiar mensaje antes de enviar
        mensaje = limpiar_mensaje(mensaje)

        # Dividir mensaje largo
        partes = split_message(mensaje)

        for i, parte in enumerate(partes, 1):
            mensaje_numerado = f"({i}/{len(partes)}) {parte}"
            print(f"Enviando parte {i}/{len(partes)} a {label} con numero: {number}")
            sim7600.send_sms(number, mensaje_numerado)
            time.sleep(1)

def main():
    try:
        #sim7600.init_modem()
        #client = mqtt_client.init_mqtt()
        #client.loop_forever()  # Escucha MQTT
        
        sim7600.init_modem()
        client, sms_queue = mqtt_client.init_mqtt()
        
        worker_thread = threading.Thread(target=sms_worker, args=(sms_queue,))
        worker_thread.daemon = True
        worker_thread.start()
        
        client.loop_forever()
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        sim7600.cleanup()

if __name__ == '__main__':
    main()
