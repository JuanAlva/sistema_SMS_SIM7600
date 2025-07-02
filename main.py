# main.py

import sim7600
import mqtt_client
import threading
import time

def sms_worker(sms_queue):
	while True:
		sms_data = sms_queue.get()
		if sms_data is None:
			break
		number = sms_data["number"]
		label = sms_data["label"]
		mensaje = sms_data["mensaje"]
		
		mensaje_final = f"{mensaje}"
		print(f"Enviando SMS a {label}, {number}")
		sim7600.send_sms(number, mensaje_final)
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
