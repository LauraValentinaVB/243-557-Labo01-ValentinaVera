from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from models.sensor import Sensor

class SensorWidget(QGroupBox):

    def __init__(self, sensor: Sensor) -> None:
        super().__init__("Capteur")

        self.sensor = sensor

        self.name_label = QLabel(self.sensor.name)
        self.value_label = QLabel("--- ")
        self.read_button = QPushButton("Lire le capteur")

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label.setStyleSheet(
            """
            font-size: 24px;
            fontweight: bold;
            padding: 12px;
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.read_button)
        self.setLayout(layout)
        self.setStyleSheet(
            """
            QGroupBox {
                border: 2px solid #6EE7B7;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
            """
)

        self.read_button.clicked.connect(self.read_sensor)

    def read_sensor(self) -> None:
        """Lit le capteur et actualise l'affichage"""
        value = self.sensor.read()
        self.value_label.setText(f"{value:.1f}{self.sensor.unit}")

        