import network
import time
from umqtt.simple import MQTTClient
 
 
SSID = "Wokwi-GUEST"
PASSWORD = ""
 
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
 
CLIENT_ID = "esp32-fiap-1ema"
TOPIC = "fiap/1ema/weather"
 
 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
 
wifi.connect(SSID, PASSWORD)
 
while not wifi.isconnected():
    print("Conectando ao Wi-Fi...")
    time.sleep(1)
 
print("Wi-Fi conectado!")
print("IP:", wifi.ifconfig()[0])
 
 
print("Conectando ao MQTT...")
 
client = MQTTClient(
    CLIENT_ID,
    MQTT_BROKER,
    port=MQTT_PORT
)
 
client.connect()
 
print("MQTT conectado!")
 
 
mensagem = '{"temperatura":25,"umidade":70,"condicao":"ensolarado"}'
 
client.publish(
    TOPIC,
    mensagem
)
 
print("Mensagem publicada!")
print("Topico:", TOPIC)
print("Mensagem:", mensagem)