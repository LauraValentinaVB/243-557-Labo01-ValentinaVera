"""Service MQTT exécuté sur le Raspberry Pi."""

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src"),
)

import paho.mqtt.client as mqtt

from config import (
    BROKER_IP,
    BROKER_PORT,
    TEAM_ID,
)
from hardware.simulation_hardware import (
    SimulationHardware,
)
from mqtt_topics import MqttTopics


class RaspberryController:
    """Relie MQTT à la couche matérielle."""

    def __init__(self) -> None:
        self.hardware = SimulationHardware()

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"raspberry-service-{TEAM_ID}",
        )

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self) -> None:
        """Démarre le service MQTT."""
        self.client.connect(BROKER_IP, BROKER_PORT)
        self.client.loop_start()

    def stop(self) -> None:
        """Arrête le service MQTT."""
        self.client.publish(
            MqttTopics.status(),
            "OFFLINE",
        )

        self.client.disconnect()
        self.client.loop_stop()

    def publish_measurements(self) -> None:
        """Publie les mesures simulées."""
        distance = self.hardware.read_sensor("Distance")
        temperature = self.hardware.read_sensor("Température")

        self.client.publish(
            MqttTopics.sensor("distance"),
            str(distance),
        )
        self.client.publish(
            MqttTopics.sensor("temperature"),
            str(temperature),
        )

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: object,
        flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None,
    ) -> None:
        """Configure le service après connexion."""
        if reason_code != 0:
            return

        self.client.subscribe(MqttTopics.command("led"))
        self.client.publish(
            MqttTopics.status(),
            "READY",
        )

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: object,
        message: mqtt.MQTTMessage,
    ) -> None:
        """Traite les commandes reçues."""
        topic = message.topic
        payload = message.payload.decode("utf-8")

        if topic == MqttTopics.command("led"):
            is_active = payload == "ON"

            self.hardware.set_actuator(
                "DEL diagnostic",
                is_active,
            )

            confirmed_payload = "ON" if is_active else "OFF"

            self.client.publish(
                MqttTopics.actuator("led"),
                confirmed_payload,
            )