class CPURegisters:
    FLAG_CARRY = 16
    FLAG_HALF_CARRY = 32
    FLAG_SUBTRACT = 64
    FLAG_ZERO = 128

    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.PC = 0
        self.SP = 0

    def get_AF(self):
        return self.A << 8 + self.F

    def set_AF(self, V):
        self.A = V >> 8
        self.F = V & 255

    def get_BC(self):
        return self.B << 8 + self.C

    def set_BC(self, V):
        self.B = V >> 8
        self.C = V & 255

    def get_DE(self):
        return self.D << 8 + self.E

    def set_DE(self, V):
        self.D = V >> 8
        self.E = V & 255

    def get_HL(self):
        return self.H << 8 + self.L

    def set_HL(self, V):
        self.H = V >> 8
        self.L = V & 255

    def flag(self, flag_type):
        return self.cpu_registers.F & flag_type

    def set_flag(self, flag_type, value):
        if value:
            self.cpu_registers.F = self.cpu_registers.F | flag_type
        else:
            self.cpu_registers.F = self.cpu_registers.F & ~flag_type

    AF = property(get_AF, set_AF)
    BC = property(get_BC, set_BC)
    DE = property(get_DE, set_DE)
    HL = property(get_HL, set_HL)