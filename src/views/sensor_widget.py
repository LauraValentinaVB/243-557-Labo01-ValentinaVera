from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from models.sensor import Sensor


class SensorWidget(QGroupBox):
    """Composant graphique représentant un capteur."""

    def __init__(self, sensor: Sensor) -> None:
        super().__init__("Capteur")

        self.sensor = sensor

        self.name_label = QLabel(self.sensor.name)
        self.value_label = QLabel("---")
        self.read_button = QPushButton("Mise à jour automatique")
        self.read_button.setEnabled(False)

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
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

    def update_value(
        self,
        value: float,
    ) -> None:
        """Actualise la valeur affichée."""
        self.value_label.setText(f"{value:.1f} {self.sensor.unit}")