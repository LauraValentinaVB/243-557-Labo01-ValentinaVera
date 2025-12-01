from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGroupBox,
    QPushButton,
)

from models.sensor import Sensor
from models.actuator import Actuator
from controllers.system_controller import SystemController
from hardware.simulation_hardware import SimulationHardware
from views.sensor_widget import SensorWidget
from views.actuator_widget import ActuatorWidget


class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")
        self.resize(700, 400)

        # Couche matérielle (une seule instance partagée)
        self.hardware = SimulationHardware()

        # Modèles
        self.sensor = Sensor(
            "Distance",
            "cm",
            self.hardware,
        )
        self.actuator = Actuator("DEL diagnostic", self.hardware)
        self.controller = SystemController(self.sensor, self.actuator)

         # Deuxième capteur
        self.temperature_sensor = Sensor(
            "Température",
            "°C",
            self.hardware,
        )

        self.title_label = QLabel("Logiciel de diagnostic - Valentina Vera")
        self.title_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
            )

        # Composants graphiques réutilisables
        self.sensor_widget = SensorWidget(self.sensor)
        self.temperature_widget = SensorWidget(self.temperature_sensor)
        self.actuator_widget = ActuatorWidget(self.actuator)
        self.sensor_widget.read_button.clicked.connect(self._apres_lecture_capteur)

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

        # ---- Layout horizontal des composants ----
        widgets_layout = QHBoxLayout()
        widgets_layout.addWidget(self.sensor_widget)
        widgets_layout.addWidget(self.actuator_widget)
        widgets_layout.addWidget(system_group)
        widgets_layout.setSpacing(20)

        widgets_layout = QHBoxLayout()
        widgets_layout.addWidget(self.sensor_widget)
        widgets_layout.addWidget(self.temperature_widget)
        widgets_layout.addWidget(self.actuator_widget)
        widgets_layout.addWidget(system_group)
        widgets_layout.setSpacing(20)

        # ---- Layout principal ----
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(widgets_layout)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # ---- Connexions des boutons système ----
        self.start_button.clicked.connect(self.demarrer_systeme)
        self.stop_button.clicked.connect(self.arreter_systeme)
        self.reset_button.clicked.connect(self.reinitialiser_systeme)

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

    def _apres_lecture_capteur(self) -> None:
        self.controller.verifier_capteur()
        self._rafraichir_interface()
        self.actuator_widget.update_display()
