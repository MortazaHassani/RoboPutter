import netifaces

# Find the wireless interface in the list of network interfaces
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
    else:
        print("Wireless interface not found")
except:
    pass