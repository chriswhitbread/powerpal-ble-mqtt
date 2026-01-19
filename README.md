# Powerpal BLE → MQTT Bridge (Raspberry Pi)

This project connects a Powerpal energy monitor to a Raspberry Pi 4 via Bluetooth Low Energy (BLE) and publishes real-time power usage to Home Assistant using MQTT.

## What it does

1. Connects to a Powerpal device over BLE  
2. Authenticates using the Powerpal pairing code  
3. Subscribes to live pulse measurements  
4. Converts pulses to instantaneous watts  
5. Publishes watts to MQTT  
6. Auto-discovers as a sensor in Home Assistant

## Architecture

Powerpal → BLE → Raspberry Pi → MQTT → Home Assistant

## Requirements

- Raspberry Pi 4 (or similar)  
- Python 3.9+  
- Bluetooth enabled  
- Home Assistant with Mosquitto MQTT broker

## Installation

```bash
git clone https://github.com/yourusername/powerpal-ble-mqtt.git
cd powerpal-ble-mqtt
python -m venv venv
source venv/bin/activate
pip install bleak paho-mqtt
```

Create `.env` from the example file and run:

```bash
python powerpal_ble_mqtt.py
```

## Home Assistant

The sensor will appear automatically via MQTT Discovery as:

`Powerpal Instant Power (W)`
