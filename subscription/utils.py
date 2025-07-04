# subscription/utils.py
import pywifi
import time

def scan_networks():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        # No Wi‑Fi adapter found or accessible
        return []

    iface = interfaces[0]
    iface.scan()
    time.sleep(2)  # Wait 2–8 seconds for scan to complete :contentReference[oaicite:1]{index=1}

    networks = []
    seen = set()
    for net in iface.scan_results():
        if net.ssid and net.ssid not in seen:
            networks.append({
                'ssid': net.ssid,
                'bssid': net.bssid,
                'signal': net.signal,
            })
            seen.add(net.ssid)
    return networks


# subscription/utils.py
from pywifi import const, Profile

def connect_to_network(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5)  # adjust timeout
    return iface.status() == const.IFACE_CONNECTED

