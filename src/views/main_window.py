from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)

from models.sensor import Sensor
from models.actuator import Actuator
from controllers.system_controller import SystemController


class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")
        self.resize(360, 260)

        self.sensor = Sensor(
            "Distance",
            "cm",
            10.0,
        )

        self.actuator = Actuator("DEL diagnostic")
        self.controller = SystemController(self.sensor, self.actuator)

        self.title_label = QLabel("Logiciel de diagnostic - Valentina Vera")

        # ----- Capteur -----
        self.sensor_name_label = QLabel(f"Nom : {self.sensor.name}")
        self.sensor_unit_label = QLabel(f"Unité : {self.sensor.unit}")
        self.sensor_value_label = QLabel("Valeur : ---")
        self.read_button = QPushButton("Lire le capteur")
        
        sensor_group = QGroupBox("Capteur")
        sensor_layout = QVBoxLayout()
        sensor_layout.addWidget(self.sensor_name_label)
        sensor_layout.addWidget(self.sensor_value_label)
        sensor_layout.addWidget(self.sensor_unit_label)
        sensor_layout.addWidget(self.read_button)
        sensor_group.setLayout(sensor_layout)

        # ---- Actionneur ----
        self.actuator_name_label = QLabel(f"Nom : {self.actuator.nom}")
        self.actuator_state_label = QLabel(self._etat_texte())
        self.toggle_button = QPushButton("Inverser l'état de l'actionneur")

        actuator_group = QGroupBox("Actionneur")
        actuator_layout = QVBoxLayout()
        actuator_layout.addWidget(self.actuator_name_label)
        actuator_layout.addWidget(self.actuator_state_label)
        actuator_layout.addWidget(self.toggle_button)
        actuator_group.setLayout(actuator_layout)

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

        # ---- Layout principal ----
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(sensor_group)
        layout.addWidget(actuator_group)
        layout.addWidget(system_group)
        self.setLayout(layout)

        # ---- Connexions des boutons ----
        self.read_button.clicked.connect(self.read_sensor)
        self.toggle_button.clicked.connect(self.toggle_actuator)
        self.start_button.clicked.connect(self.demarrer_systeme)
        self.stop_button.clicked.connect(self.arreter_systeme)
        self.reset_button.clicked.connect(self.reinitialiser_systeme)

    def read_sensor(self) -> None:
        value = self.sensor.read()
        self.sensor_value_label.setText(
            f"Valeur : {value}"
        )
        self.controller.verifier_capteur()
        self._rafraichir_interface()

    def _etat_texte(self) -> str:
        return "État : Actif" if self.actuator.actif else "État : Inactif"

    def _systeme_texte(self) -> str:
        return f"État du système : {self.controller.state}"

    def toggle_actuator(self) -> None:
        self.actuator.inverser_etat()
        self.actuator_state_label.setText(self._etat_texte())

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
        self.actuator_state_label.setText(self._etat_texte())