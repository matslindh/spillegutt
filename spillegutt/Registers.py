class CPURegisters:
    FLAG_CARRY = 16
    FLAG_HALF_CARRY = 32
    FLAG_SUBTRACT = 64
    FLAG_ZERO = 128

    AF = property(get_AF, set_AF)
    BC = property(get_BC, set_BC)
    DE = property(get_DE, set_DE)
    HL = property(get_HL, set_HL)

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

    def get_BC(self):
        return self.B << 8 + self.C

    def get_DE(self):
        return self.D << 8 + self.E

    def get_HL(self):
        return self.H << 8 + self.L

