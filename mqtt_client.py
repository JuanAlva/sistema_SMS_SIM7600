import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, PHONE_GROUPS
import sim7600
import threading
import queue
import random

sms_queue = queue.Queue()

def enviar_sms_threadsafe(phone_number, mensaje):
    # Este codigo se ejecutara en un hilo separado
    sim7600.send_sms(phone_number, mensaje)

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    # Suscribirse a todos los topicos definidos
    for topic in PHONE_GROUPS:
        client.subscribe(topic)

def on_disconnect(client, userdata, rc):
    print(f"Desconectado del broker MQTT. Codigo de retorno: {rc}")
    while rc != 0:
        try:
            print("Intentando reconexion al broker MQTT...")
            rc = client.reconnect()
            print("Reconexion exitosa.")
        except Exception as e:
            print(f"Error al reconectar: {e}")
            time.sleep(5)  # espera antes del siguiente intento

def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    topic = msg.topic
    print(f"[{topic}] Mensaje recibido: {mensaje}")
    
    if topic in PHONE_GROUPS:
        for number, label in PHONE_GROUPS[topic].items():
            sms_data = {
                "number": number,
                "label": label,
                "mensaje": mensaje
            }
            sms_queue.put(sms_data)
    else:
        print(f"Topico no reconocido: {topic}")
        
def init_mqtt():
	client_id = f"Sistema de alarmas por SMS: {random.randint(1000, 9999)}"
	client = mqtt.Client(client_id=client_id)
		
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_disconnect = on_disconnect  # callback de desconexion
	
	client.reconnect_delay_set(min_delay=2, max_delay=10)
    
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	return client, sms_queue # devuelve ambos
