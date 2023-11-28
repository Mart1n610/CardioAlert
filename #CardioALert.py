#CardioALert

#Librerias
import numpy as np
import paho.mqtt.client as mqtt

#Adafruit
adafruit_username = "Bocapasion26611"
adafruit_key = "aio_LexG82iyv2aP6x8GjouVwCE0ti3H"
adafruit_feed = "contador2"

intervalos_tiempo = []
def on_message(client, userdata, message):
    mensaje = message.payload.decode()
    print("Mensaje recibido:", mensaje)
    intervalos_tiempo.append(float(mensaje))
    calcular_frecuencia_cardiaca(intervalos_tiempo)
def calcular_frecuencia_cardiaca(intervalos_tiempo):
    if len(intervalos_tiempo) >= 2:
        promedio_intervalos = sum(intervalos_tiempo) / len(intervalos_tiempo)
        frecuencia_cardiaca = 60 / promedio_intervalos
        print(f"Frecuencia Cardíaca: {frecuencia_cardiaca} bpm")
    else:
        print("Esperando más datos para calcular la frecuencia cardíaca...")

#Configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(adafruit_username, adafruit_key)

# Conectar al servidor MQTT de Adafruit IO
client.connect("io.adafruit.com", 1883)

# Suscribirse al feed
client.subscribe(f"{adafruit_username}/feeds/{adafruit_feed}")

# Asignar la función de callback al evento on_message
client.on_message = on_message

# Iniciar el bucle de mensajes
client.loop_start()

# Mantener la ejecución del cuaderno de Colab para recibir mensajes
try:
    while True:
        pass
except KeyboardInterrupt:
    # Detener la ejecución si se presiona Ctrl+C
    client.disconnect()
    print("Desconectado por el usuario.")
except Exception as e:
    print(f"Error: {e}")