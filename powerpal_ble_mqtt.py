import asyncio
import json
import os
from bleak import BleakClient
import paho.mqtt.client as mqtt

POWERPAL_MAC = os.getenv("POWERPAL_MAC")
PAIRING_CODE = int(os.getenv("POWERPAL_PAIRING_CODE", "0"))

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

MQTT_TOPIC_WATTS = "powerpal/watts"

MEASUREMENT_CHAR = "59da0001-12f4-25a6-7d4f-55961dce4205"
READING_BATCH_CHAR = "59da0013-12f4-25a6-7d4f-55961dce4205"
PAIRING_CODE_CHAR = "59da0011-12f4-25a6-7d4f-55961dce4205"

mqtt_client = mqtt.Client()
if MQTT_USERNAME:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

def publish_discovery():
    payload = {
        "name": "Powerpal Instant Power",
        "state_topic": MQTT_TOPIC_WATTS,
        "unit_of_measurement": "W",
        "device_class": "power",
        "state_class": "measurement",
        "unique_id": "powerpal_instant_power",
        "device": {
            "identifiers": ["powerpal_energy_monitor"],
            "name": "Powerpal",
            "manufacturer": "Powerpal",
            "model": "Powerpal Energy Monitor"
        }
    }
    mqtt_client.publish(
        "homeassistant/sensor/powerpal_watts/config",
        json.dumps(payload),
        retain=True
    )

def handle_notification(_, data: bytearray):
    pulses = int.from_bytes(data[4:6], "little")
    watts = pulses * 60
    mqtt_client.publish(MQTT_TOPIC_WATTS, watts, retain=True)

async def main():
    publish_discovery()
    pairing_payload = PAIRING_CODE.to_bytes(4, "little")
    while True:
        try:
            async with BleakClient(POWERPAL_MAC, timeout=45.0) as client:
                await client.write_gatt_char(PAIRING_CODE_CHAR, pairing_payload, response=False)
                await client.write_gatt_char(READING_BATCH_CHAR, (1).to_bytes(4, "little"), response=False)
                await client.start_notify(MEASUREMENT_CHAR, handle_notification)
                while True:
                    await asyncio.sleep(1)
        except Exception as e:
            print("BLE error:", e)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
