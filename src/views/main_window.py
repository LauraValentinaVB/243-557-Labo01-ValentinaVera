from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)

from models.sensor import Sensor
from models.actuator import Actuator



class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")
        self.resize(360, 220)

        self.sensor = Sensor(
            "Distance",
            "cm",
            35.0,
        )

        self.actuator = Actuator("DEL diagnostic")
        self.title_label = QLabel("Logiciel de diagnostic - Valentina Vera")
        self.sensor_name_label = QLabel ( f"Nom : {self.sensor.name}")
        self.sensor_unit_label = QLabel(f"Unité : {self.sensor.unit}")
        self.sensor_value_label = QLabel("Valeur : ---")
        self.read_button = QPushButton("Lire le capteur")
        self.actuator_name_label = QLabel(f"Nom : {self.actuator.nom}")
        self.actuator_state_label = QLabel(self._etat_texte())
        self.toggle_button = QPushButton("Inverser l'état de l'actionneur")

        sensor_group = QGroupBox("Capteur")
        sensor_layout = QVBoxLayout()
        sensor_layout.addWidget(self.sensor_name_label)
        sensor_layout.addWidget(self.sensor_value_label)
        sensor_layout.addWidget(self.sensor_unit_label)
        sensor_layout.addWidget(self.read_button)
        sensor_group.setLayout(sensor_layout)

        actuator_group = QGroupBox("Actionneur")
        actuator_layout = QVBoxLayout()
        actuator_layout.addWidget(self.actuator_name_label)
        actuator_layout.addWidget(self.actuator_state_label)
        actuator_layout.addWidget(self.toggle_button)
        actuator_group.setLayout(actuator_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(sensor_group)
        layout.addWidget(actuator_group)
        self.setLayout(layout)

        self.setLayout(layout)

        self.read_button.clicked.connect(self.read_sensor)
        self.toggle_button.clicked.connect(self.toggle_actuator)
        

    def read_sensor(self) -> None:
        value = self.sensor.read()

        self.sensor_value_label.setText(
            f"Valeur : {value}"
        )
    def _etat_texte(self) -> str:
        return "État : Actif" if self.actuator.actif else "État : Inactif"

    def toggle_actuator(self) -> None:
        self.actuator.inverser_etat()
        self.actuator_state_label.setText(self._etat_texte)   
