import socket

def scan_network(network_prefix):
    print(f"Scanning {network_prefix}.0/24...")
    active_devices = []
    
    # 1 से 254 तक के IP एड्रेस चेक करेगा
    for i in range(1, 255):
        ip = f"{network_prefix}.{i}"
        try:
            # 1 सेकंड का समय देकर चेक करता है कि डिवाइस चालू है या नहीं
            socket.setdefaulttimeout(0.1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # आमतौर पर सीसीटीवी के पोर्ट 80, 554 या 8000 होते हैं, यहाँ हम बेसिक चेक कर रहे हैं
            result = s.connect_ex((ip, 80)) 
            if result == 0:
                print(f"Device found at: {ip}")
                active_devices.append(ip)
            s.close()
        except:
            pass
            
    return active_devices

if __name__ == "__main__":
    # अपने राउटर के हिसाब से IP सीरीज बदलें (जैसे 192.168.1)
    my_network = "192.168.1" 
    found = scan_network(my_network)
    print(f"\nकुल {len(found)} एक्टिव डिवाइस मिले।")
    
