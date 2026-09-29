from machine import Pin, I2C
from i2c_lcd import I2cLcd
import network
import time
import urequests
from umqtt.simple import MQTTClient
 
 
# ==========================================
# CONFIGURAÇÕES
# ==========================================
 
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
 
API_KEY = ""
 
CITY = "Sao Paulo"
COUNTRY = "BR"
 
 
# ==========================================
# MQTT
# ==========================================
 
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
 
CLIENT_ID = "esp32-fiap-1ema"
MQTT_TOPIC = "fiap/1ema/weather"
 
 
# ==========================================
# LCD
# ==========================================
 
i2c = I2C(
    0,
    sda=Pin(21),
    scl=Pin(22),
    freq=100000
)
 
lcd = I2cLcd(
    i2c,
    0x27,
    4,
    20
)
 
 
# ==========================================
# WI-FI
# ==========================================
 
lcd.clear()
lcd.putstr("Conectando Wi-Fi...")
 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
 
if not wifi.isconnected():
 
    wifi.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )
 
    while not wifi.isconnected():
 
        print("Conectando...")
 
        time.sleep(1)
 
 
print("Wi-Fi conectado!")
print("IP:", wifi.ifconfig()[0])
 
 
# ==========================================
# MQTT
# ==========================================
 
print("Conectando ao HiveMQ...")
 
mqtt = MQTTClient(
    CLIENT_ID,
    MQTT_BROKER,
    port=MQTT_PORT
)
 
mqtt.connect()
 
print("MQTT conectado!")
 
 
# ==========================================
# LOOP PRINCIPAL
# ==========================================
 
while True:
 
    try:
 
        # ======================================
        # CONSULTAR OPENWEATHER
        # ======================================
 
        lcd.clear()
        lcd.putstr("Consultando API...")
 
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            "?q=Sao%20Paulo%2CBR"
            "&appid=" + API_KEY
            + "&units=metric"
            + "&lang=pt"
        )
 
        print()
        print("Consultando OpenWeather...")
 
        response = urequests.get(url)
 
        print("Status HTTP:", response.status_code)
 
        if response.status_code == 200:
 
            data = response.json()
 
            temperatura = data["main"]["temp"]
            umidade = data["main"]["humidity"]
            condicao = data["weather"][0]["description"]
 
 
            # ==================================
            # LCD
            # ==================================
 
            lcd.clear()
 
            lcd.putstr("Sao Paulo")
 
            lcd.move_to(0, 1)
            lcd.putstr(
                "Temp: "
                + str(temperatura)
                + " C"
            )
 
            lcd.move_to(0, 2)
            lcd.putstr(
                "Umidade: "
                + str(umidade)
                + "%"
            )
 
            lcd.move_to(0, 3)
            lcd.putstr(
                condicao[:20]
            )
 
 
            # ==================================
            # JSON PARA MQTT
            # ==================================
 
            mensagem = (
                '{"temperatura":'
                + str(temperatura)
                + ',"umidade":'
                + str(umidade)
                + ',"condicao":"'
                + condicao
                + '"}'
            )
 
 
            print("Mensagem MQTT:")
            print(mensagem)
 
 
            # ==================================
            # PUBLICAR NO HIVEMQ
            # ==================================
 
            mqtt.publish(
                MQTT_TOPIC,
                mensagem
            )
 
            print("Mensagem publicada!")
            print("Topico:", MQTT_TOPIC)
 
 
        else:
 
            print(
                "Erro OpenWeather:",
                response.status_code
            )
 
            lcd.clear()
            lcd.putstr("API ERRO")
 
            lcd.move_to(0, 1)
            lcd.putstr(
                "HTTP: "
                + str(response.status_code)
            )
 
 
        response.close()
 
 
    except Exception as e:
 
        print()
        print("ERRO:")
        print(e)
 
        lcd.clear()
        lcd.putstr("Erro")
 
        lcd.move_to(0, 1)
        lcd.putstr(str(e)[:20])
 
 
    # ==========================================
    # AGUARDAR 10 SEGUNDOS
    # ==========================================
 
    time.sleep(10)
