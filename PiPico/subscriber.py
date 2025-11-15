"""
MQTT Temperature Subscriber - Pico 2
Subscribes to temperature topic and triggers action when threshold exceeded

Author: Mae Capacite (C21348423)
Date: 2025-11-14
"""

import machine
import time
from wifi_helper import connect_to_wifi
import config


# Initialize GPIO pin for action (LED or fan)
# GPIO 15 chosen for compatibility with external peripherals (LED/fan controller)
GPIO_PIN = 15
ACTION_PIN = machine.Pin(GPIO_PIN, machine.Pin.OUT)
ACTION_DESC = "LED/Fan control"

def import_umqtt():
    """
    Dynamically import umqtt library.
    Attempts local import first, falls back to mip.install() if not found.
    """
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
        return umqtt

def callback(topic, message):
    """
    MQTT message callback handler.

    Called when a message is received on subscribed topic.
    Triggers action if temperature exceeds threshold.

    Args:
        topic: MQTT topic (bytes)
        message: Message payload (bytes)
    """

    # Parse message with error handling for invalid data
    try:
        temp = float(message.decode('utf-8'))
    except (ValueError, UnicodeDecodeError) as e:
        print(f"Invalid message received: {message} - {e}")
        return

    print(f"Received: {temp:.2f}°C - ", end="")

    # Trigger action based on temperature threshold (default: 25°C)
    if temp >= config.TEMP_THRESHOLD:
        ACTION_PIN.value(1)
        print(f"{ACTION_DESC} ON (temp >= {config.TEMP_THRESHOLD}°C)")
    else:
        ACTION_PIN.value(0)
        print(f"{ACTION_DESC} OFF (temp < {config.TEMP_THRESHOLD}°C)")



def main():
    """Main subscriber loop: connect to WiFi and MQTT, then listen for temperature updates."""

    print("=" * 32)
    print("MQTT Temperature Subscriber - Pico 2")
    print("=" * 32)

    # Connect to WiFi
    print("\nConnecting to WiFi...")
    wifi = connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

    if not wifi:
        print("Cannot proceed without WiFi connection")
        return

    import_umqtt()

    # Initialize action pin
    print("\nInitializing action pin (GPIO 15)...")
    ACTION_PIN.value(0)  # Ensure it starts OFF
    print("Action pin ready (LED/Fan control)")

    # Set up MQTT client
    # keepalive=7000: Send keepalive ping every 7000 seconds to maintain connection
    mqtt = umqtt.MQTTClient(
        client_id=config.SUBSCRIBER_CLIENT_ID,
        server=config.MQTT_BROKER.encode(),
        port=config.MQTT_PORT,
        keepalive=7000
    )

    # Set callback and connect with error handling
    mqtt.set_callback(callback)
    try:
        mqtt.connect()
        mqtt.subscribe(config.MQTT_TOPIC)
    except OSError as e:
        print(f"Failed to connect to MQTT broker: {e}")
        print("Check broker IP and network connectivity")
        return

    print(f"Connected and subscribed to: {config.MQTT_TOPIC.decode()}")

    print("\nListening for temperature updates...")
    print(f"Threshold: {config.TEMP_THRESHOLD}°C")
    print("Press Ctrl+C to stop\n")

    # Event loop to check for messages
    # Uses non-blocking check_msg() with 100ms polling interval for responsiveness
    try:
        while True:
            mqtt.check_msg()
            time.sleep(0.1)  # 100ms polling interval balances CPU usage and responsiveness

    except KeyboardInterrupt:
        print("\n\n✓ Subscriber stopped by user")

    finally:
        # Clean up
        ACTION_PIN.value(0)  # Turn off action pin
        mqtt.disconnect()

        print("Action pin turned off")
        print("Disconnected from MQTT broker")
        print("Goodbye!")


if __name__ == "__main__":
    main()
