class Motor:
    def __init__(self, nom):
        self.nom = nom
        self.vitesse = 0
        self.distance = 0
        self.unit = "cm"
        self.state = "ON/OFF"

    def get_vitesse(self):
        return self.vitesse

    def set_vitesse(self, vitesse):
        self.vitesse = vitesse

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state



if __name__ == "__main__":
    m = Motor("Moteur A")
    print(m.get_vitesse())
    m.set_vitesse(150)
    print(m.get_vitesse())
    print(m.get_distance(), m.unit)
    print(m.get_state())

