import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, PHONE_GROUPS
import sim7600
import threading
import queue

sms_queue = queue.Queue()

def enviar_sms_threadsafe(phone_number, mensaje):
    # Este codigo se ejecutara en un hilo separado
    sim7600.send_sms(phone_number, mensaje)

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    # Suscribirse a todos los topicos definidos
    for topic in PHONE_GROUPS:
        client.subscribe(topic)

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

    
#    for number, label in LISTA_UNO.items():
#        print(f"Enviando a {label} ({number})")
#        thread = threading.Thread(target=enviar_sms_threadsafe, args=(number, mensaje))
#        thread.daemon = True
#        thread.start()
        
def init_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client, sms_queue # devuelve ambos
