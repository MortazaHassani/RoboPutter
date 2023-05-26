# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:47:48 2023

@author: Reymond
"""

import paho.mqtt.client as mqtt


class MQTTClientFYP:
    def __init__(self, broker_address, broker_port, topic, username, password):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.username = username
        self.password = password
        self.client = mqtt.Client()

        # Set the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Set MQTT client username and password
        self.client.username_pw_set(self.username, self.password)

        # Connect to the MQTT broker
        self.client.connect(self.broker_address, self.broker_port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code: " + str(rc))
        # Subscribe to the topic
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        print("Received message: " + message)
        # Perform actions based on the received message
        if message == "on":
            # Code to turn on NodeMCU-controlled device
            print("Turning on NodeMCU-controlled device")
        elif message == "off":
            # Code to turn off NodeMCU-controlled device
            print("Turning off NodeMCU-controlled device")

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def publish_message(self, message):
        self.client.publish(self.topic, message)



