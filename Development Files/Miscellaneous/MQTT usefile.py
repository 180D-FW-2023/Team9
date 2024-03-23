import paho.mqtt.client as mqtt
import numpy as np

#########           Setup               #######
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async(’test.mosquitto.org’)
client.loop_start()
#################################################


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/test")
    # The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
    print(’Unexpected Disconnect’)
    else:
    print(’Expected Disconnect’)
    # The default message callback.
    # (won’t be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))
    


client.publish(’ece180d/test’, float(np.random.random(1)), qos=1) #Send Data
# Disconnect
client.loop_stop()
client.disconnect()




