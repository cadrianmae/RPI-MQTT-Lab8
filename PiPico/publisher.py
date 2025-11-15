"""
MQTT Temperature Publisher - Pico 1
Reads temperature from RP2040 sensor and publishes to MQTT broker

Author: Mae Capacite (C21348423)
Date: 2025-11-14
"""

import time
from temp_sensor import TempSensor
from wifi_helper import connect_to_wifi
import config

def import_umqtt():
    global umqtt
    try:
        import umqtt.robust as umqtt
        return umqtt
    except ImportError:
        print("Installing umqtt.robust...")
        import mip
        mip.install("umqtt.simple")
        mip.install("umqtt.robust")
        import umqtt.robust as umqtt

def main():
    """Main publisher loop: connect to WiFi and MQTT, then publish temperature readings."""

    print("=" * 32)
    print("MQTT Temperature Publisher - Pico 1")
    print("=" * 32)

    # Connect to WiFi
    print("\nConnecting to WiFi...")
    wifi = connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

    if not wifi:
        print("Cannot proceed without WiFi connection")
        return

    import_umqtt()

    # Initialize temperature sensor
    print("\nInitializing temperature sensor...")
    temp_sensor = TempSensor()
    print(f"Sensor initialized: {temp_sensor}")

    # Initialize MQTT client
    # keepalive=7000: Send keepalive ping every 7000 seconds to maintain connection
    mqtt = umqtt.MQTTClient(
        client_id=config.PUBLISHER_CLIENT_ID,
        server=config.MQTT_BROKER.encode(),
        port=config.MQTT_PORT,
        keepalive=7000
    )

    # Connect to MQTT broker with error handling
    try:
        mqtt.connect()
        print(f"Connected to MQTT broker at {config.MQTT_BROKER}:{config.MQTT_PORT}")
    except OSError as e:
        print(f"Failed to connect to MQTT broker: {e}")
        print("Check broker IP and network connectivity")
        return

    print("\nStarting temperature publishing loop...")
    print(f"Topic: {config.MQTT_TOPIC.decode()}")
    print(f"Interval: {config.PUBLISH_INTERVAL}s")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            temp = temp_sensor.read_temp()

            # Format temperature to 2 decimal places for consistent precision
            message = f"{temp:.2f}"

            # Publish with error handling for network issues
            try:
                mqtt.publish(config.MQTT_TOPIC, message.encode())
                print(f"Published: {message}°C")
            except OSError as e:
                print(f"Publish failed: {e}, attempting reconnect...")
                mqtt.connect()

            # Wait before next reading (configurable publish interval)
            time.sleep(config.PUBLISH_INTERVAL)


    except KeyboardInterrupt:
        print("\n\nPublisher stopped by user")

    finally:
        mqtt.disconnect()
        print("Disconnected from MQTT broker")
        print("Goodbye!")


if __name__ == "__main__":
    main()
