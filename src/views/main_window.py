from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGroupBox,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import Qt

from models.sensor import Sensor
from models.actuator import Actuator
from controllers.system_controller import SystemController
from hardware.simulation_hardware import SimulationHardware
from views.sensor_widget import SensorWidget
from views.actuator_widget import ActuatorWidget
from network.mqtt_client import MqttClient
from mqtt_topics import MqttTopics


class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")
        self.resize(700, 500)

        # Couche matérielle (une seule instance partagée)
        self.hardware = SimulationHardware()

        # Modèles
        self.sensor = Sensor(
            "Distance",
            "cm",
            self.hardware,
        )
        self.temperature_sensor = Sensor(
            "Température",
            "°C",
            self.hardware,
        )
        self.actuator = Actuator("DEL diagnostic", self.hardware)
        self.controller = SystemController(self.sensor, self.actuator)

        self.title_label = QLabel("Logiciel de diagnostic - Valentina Vera")
        self.title_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        # Indicateur de connexion MQTT
        self.connection_label = QLabel("MQTT : déconnecté")
        self.connection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: darkred;
            color: white;
            """
        )

        # Composants graphiques réutilisables
        self.sensor_widget = SensorWidget(self.sensor)
        self.temperature_widget = SensorWidget(self.temperature_sensor)
        self.actuator_widget = ActuatorWidget(self.actuator)

        # ---- Système ----
        self.system_state_label = QLabel(self._systeme_texte())
        self.start_button = QPushButton("Démarrer le système")
        self.stop_button = QPushButton("Arrêter le système")
        self.reset_button = QPushButton("Réinitialiser le système")

        system_group = QGroupBox("Système")
        system_layout = QVBoxLayout()
        system_layout.addWidget(self.system_state_label)
        system_layout.addWidget(self.start_button)
        system_layout.addWidget(self.stop_button)
        system_layout.addWidget(self.reset_button)
        system_group.setLayout(system_layout)

        system_group.setStyleSheet(
            """
            QGroupBox {
                border: 2px solid #2563EB;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
            """
        )

        # ---- Journal des communications MQTT ----
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Journal des communications MQTT")

        # ---- Layout horizontal des composants ----
        widgets_layout = QHBoxLayout()
        widgets_layout.addWidget(self.sensor_widget)
        widgets_layout.addWidget(self.temperature_widget)
        widgets_layout.addWidget(self.actuator_widget)
        widgets_layout.addWidget(system_group)
        widgets_layout.setSpacing(20)

        # ---- Layout principal ----
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.connection_label)
        layout.addLayout(widgets_layout)
        layout.addWidget(self.log_view)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # ---- Connexions des boutons système ----
        self.start_button.clicked.connect(self.demarrer_systeme)
        self.stop_button.clicked.connect(self.arreter_systeme)
        self.reset_button.clicked.connect(self.reinitialiser_systeme)

        # ---- Client MQTT ----
        self.mqtt_client = MqttClient()

        self.mqtt_client.connected.connect(self.on_mqtt_connected)
        self.mqtt_client.disconnected.connect(self.on_mqtt_disconnected)
        self.mqtt_client.connection_failed.connect(self.on_mqtt_connection_failed)
        self.mqtt_client.message_received.connect(self.on_mqtt_message)

        self.actuator_widget.command_requested.connect(self.send_led_command)

        self.mqtt_client.connect_to_broker()

    def add_log(
        self,
        message: str,
    ) -> None:
        """Ajoute un message au journal."""
        self.log_view.append(message)

    def _systeme_texte(self) -> str:
        return f"État du système : {self.controller.state}"

    def demarrer_systeme(self) -> None:
        self.controller.demarrer()
        self._rafraichir_interface()

    def arreter_systeme(self) -> None:
        self.controller.arreter()
        self._rafraichir_interface()

    def reinitialiser_systeme(self) -> None:
        self.controller.reinitialiser()
        self._rafraichir_interface()

    def _rafraichir_interface(self) -> None:
        self.system_state_label.setText(self._systeme_texte())

    # ---- Gestion MQTT ----

    def on_mqtt_connected(self) -> None:
        """Traite la connexion au broker."""
        self.connection_label.setText("MQTT : connecté")
        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: green;
            color: white;
            """
        )

        self.add_log("Connexion au broker MQTT établie.")

        self.mqtt_client.subscribe(MqttTopics.sensor("distance"))
        self.mqtt_client.subscribe(MqttTopics.sensor("temperature"))
        self.mqtt_client.subscribe(MqttTopics.actuator("led"))
        self.mqtt_client.subscribe(MqttTopics.status())

    def on_mqtt_disconnected(self) -> None:
        """Traite la déconnexion du broker."""
        self.connection_label.setText("MQTT : déconnecté")
        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: darkred;
            color: white;
            """
        )

        self.add_log("Connexion MQTT fermée.")

    def on_mqtt_connection_failed(
        self,
        reason: str,
    ) -> None:
        """Traite un échec de connexion."""
        self.add_log(f"Échec de connexion MQTT : {reason}")

    def send_led_command(
        self,
        requested_state: bool,
    ) -> None:
        """Envoie une commande au Raspberry Pi."""
        payload = "ON" if requested_state else "OFF"

        self.mqtt_client.publish(
            MqttTopics.command("led"),
            payload,
        )

        self.add_log(f"Commande DEL envoyée : {payload}")

    def on_mqtt_message(
        self,
        topic: str,
        payload: str,
    ) -> None:
        """Traite un message reçu du Raspberry Pi."""
        if topic == MqttTopics.sensor("distance"):
            value = float(payload)
            self.sensor_widget.update_value(value)
            self.add_log(f"Distance reçue : {value:.1f} cm")

        elif topic == MqttTopics.sensor("temperature"):
            value = float(payload)
            self.temperature_widget.update_value(value)
            self.add_log(f"Température reçue : {value:.1f} °C")

        elif topic == MqttTopics.actuator("led"):
            is_active = payload == "ON"
            self.actuator_widget.set_state(is_active)
            self.add_log(f"État DEL confirmé : {payload}")

        elif topic == MqttTopics.status():
            self.add_log(f"État du service Raspberry : {payload}")

    def closeEvent(self, event) -> None:
        """Ferme proprement la connexion MQTT."""
        self.mqtt_client.disconnect_from_broker()
        event.accept()