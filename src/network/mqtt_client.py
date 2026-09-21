"""Client MQTT utilisé par l'outil de diagnostic."""

import paho.mqtt.client as mqtt

from PyQt6.QtCore import QObject, pyqtSignal

from config import (
    BROKER_IP,
    BROKER_PORT,
    TEAM_ID,
)


class MqttClient(QObject):
    """Gère la communication MQTT de l'application PC."""

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    connection_failed = pyqtSignal(str)

    message_received = pyqtSignal(
        str,
        str,
    )

    def __init__(self) -> None:
        super().__init__()

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"diagnostic-pc-{TEAM_ID}",
        )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def connect_to_broker(self) -> None:
        """Établit la connexion avec le broker."""
        self.client.connect(BROKER_IP, BROKER_PORT)
        self.client.loop_start()

    def disconnect_from_broker(self) -> None:
        """Ferme la connexion MQTT."""
        self.client.disconnect()
        self.client.loop_stop()

    def subscribe(self, topic: str) -> None:
        """Abonne le client à un topic."""
        self.client.subscribe(topic)

    def publish(
        self,
        topic: str,
        payload: str,
    ) -> None:
        """Publie un message MQTT."""
        self.client.publish(topic, payload)

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: object,
        flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None,
    ) -> None:
        """Traite le résultat de la connexion."""
        if reason_code == 0:
            self.connected.emit()
        else:
            self.connection_failed.emit(str(reason_code))

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: object,
        disconnect_flags: mqtt.DisconnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None,
    ) -> None:
        """Traite la déconnexion."""
        self.disconnected.emit()

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: object,
        message: mqtt.MQTTMessage,
    ) -> None:
        """Transmet un message reçu à l'application."""
        payload = message.payload.decode("utf-8")
        self.message_received.emit(
            message.topic,
            payload,
        )