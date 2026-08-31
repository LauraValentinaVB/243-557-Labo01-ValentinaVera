class Actuator:

    def __init__(self, nom):
        self.nom = nom
        self.actif = False

    def activer (self):
        self.actif = True

    def desactiver (self):
        self.actif = False

    def inverser_etat(self):
        self.actif = not self.actif

        
if __name__ == "__main__":
     a = Actuator("Lemonade")
     print(a.nom, a.actif)
     a.activer()
     print(a.nom, a.actif)
     a.inverser_etat()
     print(a.nom, a.actif)

