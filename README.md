# Lab 8: MQTT Publisher/Subscriber

**Team Members:** Mae Capacite (C21348423)
**Module:** CMPU 4100 - Fundamentals of IoT
**Date:** November 14, 2025

## Overview

This lab implements an IoT system using MQTT for temperature monitoring. Two Raspberry Pi Picos communicate via a Raspberry Pi MQTT broker.

**System Components:**
- **Raspberry Pi:** Runs Mosquitto MQTT broker
- **Pico 1 (Publisher):** Reads temperature sensor, publishes to `temp/pico` topic
- **Pico 2 (Subscriber):** Receives temperature data, turns on LED/fan when temp ≥ 25°C

## Files Included

```
PiPico/
├── config.py          # WiFi and MQTT settings
├── temp_sensor.py     # Temperature sensor class
├── wifi_helper.py     # WiFi connection utility
├── publisher.py       # Publisher script (Pico 1)
└── subscriber.py      # Subscriber script (Pico 2)

RPi/
└── mosquitto.conf     # MQTT broker config
```

## Setup

### 1. Raspberry Pi (MQTT Broker)

First, get the Raspberry Pi's IP address:
```bash
# On the Raspberry Pi
hostname -I
```

Install Mosquitto and copy the config file:

```bash
# On your laptop
scp RPi/mosquitto.conf pi@<raspberry-pi-ip>:/tmp/mosquitto.conf

# SSH into the Pi
ssh pi@<raspberry-pi-ip>

# On the Raspberry Pi
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo mv /tmp/mosquitto.conf /etc/mosquitto/mosquitto.conf
sudo systemctl restart mosquitto
```

### 2. Pico Configuration

Update `PiPico/config.py` with your WiFi credentials and Raspberry Pi IP address.

Install the MQTT library on both Picos:
```python
import mip
mip.install("umqtt.robust")
```

### 3. Deploy to Picos

Copy files to each Pico using Thonny or mpremote:
- **Pico 1:** Copy all files from `PiPico/`, run `publisher.py`
- **Pico 2:** Copy all files from `PiPico/`, run `subscriber.py`

## Running the System

1. Start the subscriber on Pico 2
2. Start the publisher on Pico 1
3. Temperature readings will be published every 2 seconds
4. When temperature exceeds 25°C, the subscriber triggers GPIO pin 15 (LED/fan)

## Testing the Broker

You can test the broker independently using the mosquitto clients:

```bash
# Subscribe to messages (Terminal 1)
mosquitto_sub -h localhost -t temp/pico

# Publish a test message (Terminal 2)
mosquitto_pub -h localhost -t temp/pico -m "26.5"
```
