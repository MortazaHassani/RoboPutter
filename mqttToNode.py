import paho.mqtt.client as mqtt



# MQTT broker details

broker_address = "192.168.137.212"  # Replace with your MQTT broker IP address

broker_port = 1883

topic = "nodemcu/control"  # Replace with the desired topic



# MQTT client username and password

username = "golf"  # Replace with the MQTT client username

password = "golf123"  # Replace with the MQTT client password



# Callback function for MQTT connection

def on_connect(client, userdata, flags, rc):

    print("Connected to MQTT broker with result code: " + str(rc))

    # Subscribe to the topic

    client.subscribe(topic)



def on_message(client, userdata, msg):

    message = msg.payload.decode("utf-8")

    print("Received message: " + message)

    # Perform actions based on the received message

    if message == "on":

        # Code to turn on NodeMCU-controlled device

        print("Turning on NodeMCU-controlled device")

    elif message == "off":

        # Code to turn off NodeMCU-controlled device

        print("Turning off NodeMCU-controlled device")





# Create MQTT client instance

client = mqtt.Client()



# Set the callback functions

client.on_connect = on_connect

client.on_message = on_message



# Set MQTT client username and password

client.username_pw_set(username, password)



# Connect to the MQTT broker

client.connect(broker_address, broker_port, 60)



client.loop_start()



# Keep the script running

mqtt_message = ""
while (mqtt_message != "exit"):
    mqtt_message = input("Enter msg: ")
    client.publish('golf/leds/esp8266', mqtt_message)