from Registers import CPURegisters, HardwareRegisters
from Memory import Memory

class CPU:
    def __init__(self):
        self.cpu_registers = CPURegisters()
        self.hw_registers = HardwareRegisters()
        self.memory = Memory(self.hw_registers)

    def flag(self, flag_type):
        return self.F & flag_type

    def set_flag(self, flag_type):
        self.F = self.F | flag_type

    def reset_flag(self, flag_type):
        self.F = self.F & ~flag_type
