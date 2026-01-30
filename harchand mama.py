import socket
import subprocess
import concurrent.futures
import time

# --- Colors ---
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def get_device_type(ip):
    # RTSP Port 554 (Cameras)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((ip, 554)) == 0:
            s.close()
            return f"{RED}📹 Camera (RTSP){RESET}"
        s.close()
    except:
        pass

    # HTTP Port 80 (Router/DVR)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((ip, 80)) == 0:
            s.close()
            return f"{GREEN}🌐 Router/DVR/Web{RESET}"
        s.close()
    except:
        pass
    
    return f"{CYAN}📱 Mobile/PC{RESET}"

def scan_ip(ip_info):
    base_ip, ip_end = ip_info
    ip = f"{base_ip}.{ip_end}"
    try:
        output = subprocess.call(['ping', '-c', '1', '-W', '1', ip], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        if output == 0:
            dtype = get_device_type(ip)
            return (ip, dtype)
    except:
        pass
    return None

# --- यहाँ से "Loop" (चक्र) शुरू होता है ---
while True:
    # 1. स्क्रीन साफ़ (Refresh Effect)
    print("\033[H\033[J")
    print(f"{GREEN}=========================================={RESET}")
    print(f"{GREEN}   BN CCTV - HAR CHAND MA SCANNER 🔄   {RESET}")
    print(f"{GREEN}=========================================={RESET}")

    # 2. IP पता करना
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        my_ip = s.getsockname()[0]
        s.close()
    except:
        my_ip = "192.168.1.x"

    base_ip = my_ip.rsplit('.', 1)[0]
    print(f"[*] आपका IP: {CYAN}{my_ip}{RESET}")
    print(f"{YELLOW}[*] स्कैनिंग चालू... कृपया रुकें...{RESET}")
    print("-" * 42)

    found_devices = []
    start_time = time.time()

    # 3. स्कैनिंग
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # base_ip भी साथ भेज रहे हैं
        results = executor.map(scan_ip, [(base_ip, i) for i in range(1, 255)])
        
        for result in results:
            if result:
                ip, dtype = result
                print(f"Found: {ip} -> {dtype}")
                found_devices.append(result)

    found_devices.sort(key=lambda x: int(x[0].split('.')[-1]))
    end_time = time.time()
    
    # 4. रिपोर्ट
    print("\n" + "-" * 42)
    print(f"{YELLOW}========= 📋 फाइनल रिपोर्ट ========={RESET}")
    print(f"Time: {round(end_time - start_time, 2)}s | Total: {len(found_devices)}")
    print("-" * 42)

    for ip, dtype in found_devices:
        if ip == my_ip:
            print(f"📲 {ip} \t<-- आप")
        else:
            print(f"{ip} \t: {dtype}")

    print(f"{GREEN}=========================================={RESET}")
    
    # 5. रिफ्रेश करने का जादू 🪄
    print(f"\n{RED}[REFRESH]{RESET} दोबारा स्कैन करने के लिए {YELLOW}Enter{RESET} दबाएं...")
    print(f"(बाहर निकलने के लिए 'q' दबाकर Enter करें)")
    
    choice = input()
    if choice.lower() == 'q':
        break
    
    print("रिफ्रेश हो रहा है...")
    time.sleep(0.5)
