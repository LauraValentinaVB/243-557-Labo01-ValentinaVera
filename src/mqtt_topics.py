"""Topics MQTT utilisés par le système."""

from config import MQTT_ROOT


class MqttTopics:
    """Construit les topics officiels du système."""

    @staticmethod
    def command(name: str) -> str:
        """Retourne le topic d'une commande."""
        return f"{MQTT_ROOT}/commands/{name}"

    @staticmethod
    def actuator(name: str) -> str:
        """Retourne le topic d'état d'un actionneur."""
        return f"{MQTT_ROOT}/actuators/{name}"

    @staticmethod
    def sensor(name: str) -> str:
        """Retourne le topic d'un capteur."""
        return f"{MQTT_ROOT}/sensors/{name}"

    @staticmethod
    def status() -> str:
        """Retourne le topic d'état général."""
        return f"{MQTT_ROOT}/status"

    @staticmethod
    def diagnostic(name: str) -> str:
        """Retourne le topic d'une information de diagnostic."""
        return f"{MQTT_ROOT}/diagnostics/{name}"

    @staticmethod
    def event(name: str) -> str:
        """Retourne le topic d'un événement."""
        return f"{MQTT_ROOT}/events/{name}"