import winreg
import subprocess
import os

class SysAdmin:
    def __init__(self):
        pass

    def read_registry(self, path, key_name):
        """Reads a value from the Windows Registry."""
        try:
            # Split path (e.g., HKEY_CURRENT_USER\Software\...)
            root_str, sub_path = path.split('\\', 1)
            root = getattr(winreg, root_str)
            with winreg.OpenKey(root, sub_path) as key:
                value, _ = winreg.QueryValueEx(key, key_name)
                return f"Registry Value: {value}"
        except Exception as e:
            return f"Registry Error: {e}"

    def list_services(self):
        """Lists active Windows services using sc query."""
        try:
            res = subprocess.check_output("sc query state= all", shell=True).decode('utf-8', errors='ignore')
            # Extract names only for brevity
            names = [line.split(":")[1].strip() for line in res.split('\n') if "SERVICE_NAME" in line]
            return names[:20] # Return first 20 for context
        except: return []

    def get_network_info(self):
        """Gets Wi-Fi name and local IP."""
        try:
            res = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8', errors='ignore')
            ssid = [line.split(":")[1].strip() for line in res.split('\n') if "SSID" in line and "BSSID" not in line]
            return f"Connected to: {ssid[0] if ssid else 'Ethernet/None'}"
        except: return "Network status unavailable."

    def list_ports(self):
        """Lists active network connections."""
        try:
            res = subprocess.check_output("netstat -ano", shell=True).decode('utf-8', errors='ignore')
            return res.split('\n')[:15] # Top 15 connections
        except: return []
