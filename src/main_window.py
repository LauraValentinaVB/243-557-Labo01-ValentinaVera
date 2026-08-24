from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from sensor import Sensor


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

        self.title_label = QLabel("Logiciel de diagnostic - Valentina Vera")
        self.sensor_name_label = QLabel ( f"Nom : {self.sensor.name}")
        self.sensor_unit_label = QLabel(f"Unité : {self.sensor.unit}")
        self.sensor_value_label = QLabel("Valeur : ---")
        self.read_button = QPushButton("Lire le capteur")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.sensor_name_label)
        layout.addWidget(self.sensor_value_label)
        layout.addWidget(self.sensor_unit_label)
        layout.addWidget(self.read_button)

        self.setLayout(layout)

        self.read_button.clicked.connect(self.read_sensor)

    def read_sensor(self) -> None:
        value = self.sensor.read()

        self.sensor_value_label.setText(
            f"Valeur : {value}"
        )
