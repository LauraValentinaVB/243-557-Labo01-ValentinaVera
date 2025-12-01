import random


class SimulationHardware:

    def __init__(self) -> None:
        self.actuator_states: dict[str, bool] = {}

    def read_sensor(self, sensor_name: str) -> float:

        if sensor_name == "Distance":
            return round(random.uniform(10.0, 100.0), 1)

        if sensor_name == "Température":
            return round(random.uniform(18.0, 30.0), 1)

        return 0.0

    def set_actuator(
        self,
        actuator_name: str,
        is_active: bool,
    ) -> None:

        self.actuator_states[actuator_name] = is_active