class RaspberryHardware:

    def read_sensor(
        self,
        sensor_name: str,
    ) -> float:
        """Lit un capteur réel."""
        # À compléter dans
        # un prochain laboratoire.
        raise NotImplementedError(
            "La lecture matérielle "
            "n'est pas encore implantée."
        )

    def set_actuator(
        self,
        actuator_name: str,
        is_active: bool,
    ) -> None:
        """Commande un actionneur réel."""
        # À compléter dans
        # un prochain laboratoire.
        raise NotImplementedError(
            "La commande matérielle "
            "n'est pas encore implantée."
        )