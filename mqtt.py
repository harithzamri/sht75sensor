import paho.mqtt.client as mqttClient
import time
from sht_sensor import Sht

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to the broker")
        global Connected
        Connected = True
    else:
        print ("connection failed")

Connected = False

broker_address = "m14.cloudmqtt.com"
port = 16207
user = "eeyukxqp"
password = "DylaiZ3nfPHL"
client = mqttClient.Client("Python")

client.username_pw_set(user, password=password)
client.on_connect=on_connect()

client.connect(broker_address, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

try:
    while True:
        sht = Sht(24,23)
        temperature = float(sht.read_t())
        humidity = float(sht.read_rh())

        time.sleep(10)
        client.publish("python/temperature", temperature)
        client.publish("python/humidity", humidity)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
