from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from models.actuator import Actuator

class ActuatorWidget(QGroupBox):
    """Composant graphique représentant un actionneur"""

    def __init__(self, actuator: Actuator) -> None:
        super().__init__("Actionneur")

        self.actuator = actuator

        self.name_label = QLabel(self.actuator.nom)
        self.state_label = QLabel()
        self.toggle_button = QPushButton()

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.state_label)
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)
        self.setStyleSheet(
            """
            QGroupBox {
                border: 2px solid #DC2626;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
            """
)

        self.toggle_button.clicked.connect(self.toggle_actuator)

        self.update_display()

    def toggle_actuator(self) -> None:
        """Inverse l'état de l'actionneur."""
        self.actuator.inverser_etat()
        self.update_display()

    def update_display(self) -> None:
        """Actualise le texte et l'apparence."""
        if self.actuator.actif:
            self.state_label.setText("ACTIF")
            self.toggle_button.setText("Désactiver")
            self.state_label.setStyleSheet(
                """
                font-size: 24px;
                font-weight: bold;
                padding: 12px;
                background-color: #C4B5FD;
                color: #4C1D95;
                """
            )
        else:
            self.state_label.setText("INACTIF")
            self.toggle_button.setText("Activer")
            self.state_label.setStyleSheet(
                """
                font-size: 24px;
                font-weight: bold;
                padding: 12px;
                background-color: #E9D5FF;
                color: #6B21A8;
                """
            )