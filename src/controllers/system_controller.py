class SystemController:
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    ALARM = "ALARM"

    SEUIL_ALARME = 80

    def __init__(self, sensor, actuator):
        self.sensor = sensor
        self.actuator = actuator
        self.state = self.STOPPED

    def demarrer(self) -> None: 
        print(self.STOPPED)
        print(type(self.STOPPED))
        if self.state == self.STOPPED:
            self.state = self.RUNNING

    def arreter(self) -> None:
        if self.state == self.RUNNING:
            self.state = self.STOPPED

    def reinitialiser(self) -> None:
        if self.state == self.ALARM:
            self.state = self.STOPPED
            self.actuator.desactiver()

    def verifier_capteur(self) -> None:
        if self.state == self.RUNNING and self.sensor.read()  > self.SEUIL_ALARME:
            self.state = self.ALARM
            self.actuator.activer()
