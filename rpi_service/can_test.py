import time
from can_manager import CanManager

can = CanManager("can0")
can.open()

def esperar(id_esperado, timeout=1.0):
    fin = time.time() + timeout
    while time.time() < fin:
        msg = can.receive(timeout=0.1)
        if msg is not None and msg.arbitration_id == id_esperado:
            return msg
    return None

try:
    print("TX : commande LED ON")
    can.send(0x100, [0x01])
    r = esperar(0x210)
    print(f"RX : 0x210 ACK={r.data[0]}" if r else "RX : pas d'ACK")

    time.sleep(0.5)

    print("TX : commande LED OFF")
    can.send(0x100, [0x00])
    r = esperar(0x210)
    print(f"RX : 0x210 ACK={r.data[0]}" if r else "RX : pas d'ACK")

    print("TX : demande compteur")
    can.send(0x101, [])
    r = esperar(0x201)
    if r:
        valeur = (r.data[0] << 8) | r.data[1]
        print("RX : 0x201")
        print(f"Valeur : {valeur}")
    else:
        print("RX : pas de valeur")
finally:
    can.close()
