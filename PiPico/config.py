"""
Configuration file for MQTT Lab 8
Loads settings from .env file in repo root

Author: Mae Capacite (C21348423)
Date: 2025-11-14
"""

import os


def load_env_file(filepath="../../.env") -> dict[str, str]:
    """
    Load environment variables from .env file.

    Simple implementation for MicroPython compatibility.
    Does not use external libraries like python-dotenv.
    """
    env_vars: dict[str, str] = {}

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=VALUE format
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

    except OSError:
        # .env file doesn't exist - use defaults
        print("Warning: .env file not found, using default values")
        return {}

    return env_vars


# Load environment variables
_env = load_env_file()

# WiFi Configuration
WIFI_SSID = _env.get("WIFI_SSID", "Wokwi-GUEST")
WIFI_PASSWORD = _env.get("WIFI_PASSWORD", "")

# MQTT Broker Configuration
MQTT_BROKER = _env.get("MQTT_BROKER", "192.168.1.100")
MQTT_PORT = int(_env.get("MQTT_PORT", "1883"))
MQTT_TOPIC = _env.get("MQTT_TOPIC", "temp/pico").encode()

# Publisher Configuration
PUBLISHER_CLIENT_ID = _env.get("PUBLISHER_CLIENT_ID", "publisher").encode()
PUBLISH_INTERVAL = int(_env.get("PUBLISH_INTERVAL", "2"))

# Subscriber Configuration
SUBSCRIBER_CLIENT_ID = _env.get("SUBSCRIBER_CLIENT_ID", "subscriber").encode()
TEMP_THRESHOLD = float(_env.get("TEMP_THRESHOLD", "25.0"))
