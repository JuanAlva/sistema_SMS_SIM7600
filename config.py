# config.py

MQTT_BROKER = '192.168.148.67'  # o IP de broker EMQX
MQTT_PORT = 1883

# Topicos
TOPIC_ALARMA1 = 'alarma/lista1'
TOPIC_ALARMA2 = 'alarma/lista2'

# Lista de destinatarios
PHONE_GROUPS = {
	TOPIC_ALARMA1: {
		'51918518421': 'Jose Sanchez',
		'51972095270': 'David Ninamancco'
				
	},
	TOPIC_ALARMA2: {
		'51922012761': 'Jhoan Medina',
		'51981212690': 'Irvin Meza',
		'51907345842': 'Angie',
		'51992789961': 'Johan Ramirez',
		'51995091099': 'Fray'
	}
}

SERIAL_PORT = '/dev/ttyS0'
BAUD_RATE = 115200
POWER_KEY_GPIO = 6
