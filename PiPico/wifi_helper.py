"""
WiFi connection helper for Raspberry Pi Pico W
Handles WiFi connectivity with timeout and status reporting

Author: Mae Capacite (C21348423)
Date: 2025-11-14
"""

import network
import time


def connect_to_wifi(ssid: str, password: str, timeout: int = 10) -> network.WLAN:
    """
    Connect to WiFi network with given credentials.

    Args:
        ssid: WiFi network name
        password: WiFi password
        timeout: Maximum time to wait for connection (seconds)

    Returns:
        WLAN object if connected, None if failed
    """
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    print(f"Connecting to {ssid}...", end="")

    while not wifi.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

    if wifi.isconnected():
        ip = wifi.ifconfig()[0]
        print(f"\n✓ Connected! IP: {ip}")
        return wifi

    print("\nFailed to connect to WiFi")
    return None
