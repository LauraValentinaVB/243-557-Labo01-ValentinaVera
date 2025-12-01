class Sensor:
    def __init__(
            self,
            name: str,
            unit: str,
            hardware,
    ) -> None:
            self.name = name
            self.unit = unit
            self.hardware = hardware

    def read(self) -> float:
        return self.hardware.read_sensor(self.name)
    
        