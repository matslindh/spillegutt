class Memory:
    def __init__(self, hw_registers):
        self.hw_registers = hw_registers
        self.memory = bytearray(65536)
