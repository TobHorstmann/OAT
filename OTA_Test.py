from machine import SoftI2C, Pin, deepsleep
from AHT10 import AHT10
from umqtt.simple import MQTTClient
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
import network
import time
import json

#################################################################################################################

firmware_url = "https://raw.githubusercontent.com/TobHorstmann/OAT/"
ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "OTA_Test.py")

#################################################################################################################

# I2C und Sensor initialisieren
i2c = SoftI2C(scl=Pin(1), sda=Pin(2))
sensor_aht10 = AHT10(i2c)

#################################################################################################################

# MQTT-Daten
BROKER = "192.168.1.212"
PORT = 1883
TOPIC = "BZTG"
CLIENT_ID = "ESP_32"

#################################################################################################################

# Hauptprogramm
try:
    
    #OAT

    ota_updater.download_and_install_update_if_available()
    
    client = MQTTClient(CLIENT_ID, BROKER, PORT)
    client.connect()
    print(f"MQTT verbunden mit {BROKER}")

    temperatur = round(sensor_aht10.temperature())
    feuchtigkeit = round(sensor_aht10.humidity())

    data = {
        "Temperatur": temperatur,
        "Feuchtigkeit": feuchtigkeit
    }

    json_data = json.dumps(data)
    client.publish(TOPIC, json_data)
    print(f"Daten gesendet: {json_data}")

    client.disconnect()
    wlan.disconnect()
    print("Gehe in Deep Sleep für 55 Sekunden...")

    time.sleep(1)  # kurz warten, damit alles sicher abgeschlossen ist
    deepsleep(55000)

except Exception as e:
    print("Fehler:", e)
    # Optional: etwas kürzer schlafen, um schneller erneut zu starten
    deepsleep(10000)