import time
import json
from get_secrets import get_secrets, get_host
import paho.mqtt.client as paho
from paho import mqtt


#############################
# SETTING UP THE MESSAGE AND TAGS
#############################

tag = "equipo/37/dispositivo/2"
message = "temperatura dispositivo 2"


#create a class that does all the on_connect, on_publish, etc. stuff
class MQTTClient:
    def __init__(self, client_id, username, password, host):
        self.client_id = client_id
        self.username = username
        self.password = password
        self.host = host
        self.client = paho.Client(client_id=self.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.connect(host, 8883)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def publish(self, topic, payload, qos=0, retain=False, properties=None):
        self.client.publish(topic, payload, qos, retain, properties)

    def subscribe(self, topic, qos=0, options=None, properties=None):
        self.client.subscribe(topic, qos, options, properties)

    def loop_forever(self):
        self.client.loop_forever()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()


if __name__ == "__main__":

    username, password = get_secrets()
    host = get_host()
    # funtion that creates random temperature data from 30 to 40 degrees
    def get_temperature():
        import random
        return random.randint(30, 40)

    # initiate the MQQTClient class
    client = MQTTClient(client_id="", username=username, password=password, host=host)
    i = 0
    while i < 100:
        # a single publish, this can also be done in loops, etc.
        payload = json.dumps({message: f"{get_temperature()} grados"})
        client.publish(f"{tag}", payload=payload, qos=0)
        time.sleep(1)
        i +=1


    # disconnect from the broker
    client.disconnect()
