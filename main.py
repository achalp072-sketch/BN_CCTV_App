
import tkinter as tk
from tkinter import ttk
import socket
import threading
import os

class BN_CCTV_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("BN CCTV SECURITY")
        self.root.geometry("360x640")
        self.root.configure(bg='#000')

        tk.Label(root, text="BN CCTV SECURITY", fg='#0F0', bg='#000', font=("Arial", 16, "bold")).pack(pady=10)
        self.my_ip = self.get_ip()
        tk.Label(root, text=f"My IP: {self.my_ip}", fg='#FFF', bg='#333').pack(pady=5)

        tk.Button(root, text="AUTO SCAN", bg='#1976D2', fg='#FFF', font=("Arial", 10, "bold"), width=20, command=self.start_auto).pack(pady=5)
        
        self.ip_entry = tk.Entry(root, justify='center', font=("Arial", 12), bg='#111', fg='yellow')
        self.ip_entry.insert(0, ".".join(self.my_ip.split('.')[:-1]))
        self.ip_entry.pack(pady=5)

        tk.Button(root, text="FORCE SCAN", bg='#FFB300', fg='#000', font=("Arial", 10, "bold"), width=20, command=self.start_force).pack(pady=5)
        tk.Button(root, text="STOP SCAN", bg='#D32F2F', fg='#FFF', font=("Arial", 10, "bold"), width=20, command=self.stop_scan).pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("T", "IP", "S"), show='headings')
        self.tree.heading("T", text="TYPE"); self.tree.heading("IP", text="IP"); self.tree.heading("S", text="SECURITY")
        self.tree.column("T", width=90); self.tree.column("IP", width=110); self.tree.column("S", width=110)
        self.tree.pack(pady=10, padx=5, fill="both", expand=True)
        
        self.tree.tag_configure('danger', foreground='red')
        self.tree.tag_configure('safe', foreground='green')
        self.is_scanning = False

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except: return "127.0.0.1"

    def detect_device_type(self, ip):
        last = int(ip.split('.')[-1])
        if last == 1: return "Router"
        elif 100 <= last <= 150: return "CCTV Camera"
        else: return "Mobile/PC"

    def scan_logic(self, prefix):
        self.is_scanning = True
        self.root.after(0, lambda: [self.tree.delete(i) for i in self.tree.get_children()])
        for i in range(1, 255):
            if not self.is_scanning: break
            ip = f"{prefix}.{i}"
            res = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
            if res == 0:
                d_type = self.detect_device_type(ip)
                status = "SAFE ✅" if d_type == "CCTV Camera" else "RISK/VIRUS ⚠️"
                tag = 'safe' if status == "SAFE ✅" else 'danger'
                self.root.after(0, lambda t=d_type, ip=ip, s=status, g=tag: self.tree.insert('', 'end', values=(t, ip, s), tags=(g,)))
        self.is_scanning = False

    def start_auto(self):
        pre = ".".join(self.my_ip.split('.')[:-1])
        threading.Thread(target=self.scan_logic, args=(pre,), daemon=True).start()

    def start_force(self):
        threading.Thread(target=self.scan_logic, args=(self.ip_entry.get(),), daemon=True).start()

    def stop_scan(self): self.is_scanning = False

if __name__ == "__main__":
    root = tk.Tk()
    app = BN_CCTV_Final(root)
    root.mainloop()
