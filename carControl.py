import json
import platform
import socket
import netifaces
import sys
from MQTTClientFYP import MQTTClientFYP
import keyboard
import time


json_location = 'setting.json'
with open(json_location) as jfile:
    setting = json.load(jfile)
def update_setting(settingf = setting):
    with open(json_location, 'w') as ujfile:
        json.dump(settingf, ujfile)


def get_ip(setting):
    try:
        interfaces = netifaces.interfaces()
        wireless_interface = None
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
                if addrs[netifaces.AF_LINK][0]['addr'].startswith('b8:27:eb'):
                    if addrs[netifaces.AF_INET][0]['addr'].startswith('192.168.'):
                        wireless_interface = iface
                        break

        # Get the IP address of the wireless interface

        if wireless_interface is not None:
            ip_address = netifaces.ifaddresses(wireless_interface)[netifaces.AF_INET][0]['addr']
            print("IP address:", ip_address)
            setting['MQTT']['pi_ip'] = ip_address
            update_setting(setting)
        else:
            print("Wireless interface not found")
    except:
        pass

def forward(degree_c = setting['car']['degree_change']):
  return "forward " + str(degree_c)

def backward(degree_c = setting['car']['degree_change']):
  return "backward " + str(degree_c)

def left(degree_c = setting['car']['degree_change']):
  return "left " + str(degree_c)

def right(degree_c = setting['car']['degree_change']):
  return "right " + str(degree_c)

def kick(kick_degree=180):
    return "kick " + str(kick_degree)
def zero_kick(kick_degree=0):
    return "kick " + str(kick_degree)

arrow_keys = {
  "up": forward,
  "down": backward,
  "left": left,
  "right": right,
  "k": kick,
  "z":zero_kick

}


def command_car(setting, command_d):
    try:        
        client = MQTTClientFYP(
        broker_address=setting['broker']['broker_address'],
        broker_port=setting['broker']['broker_port'],
        topic=setting['broker']['topic'],
        username=setting['broker']['username'],
        password=setting['broker']['password']
        )

        client.start()
        print('MQTT initialized', flush=True)

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                # print(event.name)
                if event.name == "esc":
                    break
                try:
                    command_d = arrow_keys[event.name]()
                    client.publish_message(command_d)
                    # print(command_d)
                except:
                    print('wrong key')
                
                
        client.stop()

        # while (command_d != 0 or command_d != "0"): 
        #     command_d = input("Enter Command: ")
        #     if len(command_d) != 0:
        #         client.publish_message(command_d)
        # client.stop()
    except Exception as e:
        print(f'MQTT connection issue: {e}', flush=True)

if __name__ == '__main__':
    get_ip(setting)
    command_car(setting, "1")
