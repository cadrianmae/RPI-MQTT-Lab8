# Deployment Notes

Instructions for deploying the MQTT system to hardware.

## Configuration

Edit `PiPico/config.py` with your WiFi credentials and Raspberry Pi IP address:

```python
WIFI_SSID = "YourNetworkName"
WIFI_PASSWORD = "YourPassword"
MQTT_BROKER = "192.168.1.100"  # Use hostname -I on your Pi
```

## Deploying to Raspberry Pi

1. Copy the mosquitto config file to your Pi:
   ```bash
   scp RPi/mosquitto.conf pi@192.168.1.100:/tmp/mosquitto.conf
   ```

2. SSH into your Pi and move the file:
   ```bash
   ssh pi@192.168.1.100
   sudo mv /tmp/mosquitto.conf /etc/mosquitto/mosquitto.conf
   sudo systemctl restart mosquitto
   ```

3. Check it's running:
   ```bash
   sudo systemctl status mosquitto
   ```

## Deploying to Picos

Upload files manually using Thonny or mpremote.

**For Publisher (Pico 1):**
```bash
mpremote cp config.py :config.py
mpremote cp temp_sensor.py :temp_sensor.py
mpremote cp wifi_helper.py :wifi_helper.py
mpremote cp publisher.py :main.py
```

**For Subscriber (Pico 2):**
```bash
mpremote cp config.py :config.py
mpremote cp wifi_helper.py :wifi_helper.py
mpremote cp subscriber.py :main.py
```

## Common Issues

**WiFi not connecting:**
- Double-check SSID and password in config.py
- Make sure you're using 2.4GHz network (Pico W doesn't support 5GHz)

**MQTT connection fails:**
- Verify the Raspberry Pi IP address is correct
- Check Mosquitto is running: `sudo systemctl status mosquitto`
- Try testing with mosquitto_pub/sub commands first

**No temperature readings:**
- Check the serial output for error messages
- Make sure umqtt.robust is installed on the Pico
