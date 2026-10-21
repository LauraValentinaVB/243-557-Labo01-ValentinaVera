import can

class CanManager:
    def __init__(self, channel="can0"):
        self.channel = channel
        self.bus = None

    def open(self):
        self.bus = can.Bus(interface="socketcan", channel=self.channel)

    def send(self, can_id, data):
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
        self.bus.send(msg)

    def receive(self, timeout=1.0):
        return self.bus.recv(timeout=timeout)

    def close(self):
        if self.bus is not None:
            self.bus.shutdown()
            self.bus = None
