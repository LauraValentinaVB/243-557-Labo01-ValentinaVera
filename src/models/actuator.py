class Actuator:

    def __init__(self, nom, hardware):
        self.nom = nom
        self.hardware = hardware
        self.actif = False

    def activer (self):
        self.actif = True
        self.hardware.set_actuator(self.nom, self.actif)

    def desactiver (self):
        self.actif = False
        self.hardware.set_actuator(self.nom, self.actif)

    def inverser_etat(self):
        if self.actif:
            self.desactiver()
        else:
            self.activer()
    

