from Registers import CPURegisters, HardwareRegisters
from Memory import Memory
from functools import partial

class CPU:
    def __init__(self):
        self.cpu_registers = CPURegisters()
        self.hw_registers = HardwareRegisters()
        self.memory = Memory(self.hw_registers)

        self.ops = {
            0x00: (1, self.instr_nop),
            0x01: (1, self.instr_ld_bc),
            0x02: (1, self.instr_ld_bci_a),
            0x03: (1, self.instr_inc_bc),
            0x04: (1, self.instr_inc_b),
            0x05: (1, self.instr_dec_b),
            0x06: (1, self.instr_ld_b),
            0x07: (1, self.instr_rlc_c),
            0x08: (1, self.instr_ld_nn_sp),
            0x09: (1, self.instr_add_hl_bc),
            0x0A: (1, self.instr_ld_a_bci),
            0x0B: (1, self.instr_dec_bc),
            0x0C: (1, self.instr_inc_c),
            0x0D: (1, self.instr_dec_c),
            0x0E: (1, self.instr_ld_c),
            0x0F: (1, self.instr_rrc_a),
        }

    def execute(self):
        cycles, instr = self.ops[self.get_8b_from_PC()]]
        self.increment_PC(1)
        instr()

    def instr_nop(self):
        return

    def instr_ld_bc(self):
        self.cpu_registers.BC = self.get_16b_from_PC()
        self.increment_PC(2)

    def instr_ld_bci_a(self):
        self.memory[self.cpu_registers.BC] = self.cpu_registers.A

    def instr_inc_bc(self):
        self.cpu_registers.BC += 1

    def instr_inc_b(self):
        self.cpu_registers.B += 1

    def instr_dec_b(self):
        self.cpu_registers.B -= 1

    def instr_ld_b(self):
        self.cpu_registers.B = self.get_8b_from_PC()

    def instr_rlc_c(self):
        self.cpu_registers.C = self.rlc_it(self.cpu_registers.C)

    def instr_ld_nn_sp(self):
        self.memory[self.get_16b_from_PC()] = self.stack.pop()

    def rlc_it(self, value):
        if value & 128:
            self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY)
        else:
            self.cpu_registers.reset_flag(self.cpu_registers.FLAG_CARRY)

        return value << 1 + ((value & 128) >> 7)

    def get_8b_from_PC(self):
        return self.memory[self.cpu_registers.PC]

    def get_16b_from_PC(self):
        return self.memory[self.cpu_registers.PC] << 8 + self.memory[self.cpu_registers.PC+1]

    def pop_16b_from_stack(self):
        value = self.memory[self.cpu_registers.SP] << 8 + self.memory[self.cpu_registers.SP+1]
        self.cpu_registers.SP -= 2

        return value

    def push_16b_on_stack(self, val):
        self.memory[self.cpu_registers.SP] = val & 255
        self.memory[self.cpu_registers.SP+1] = val >> 8
        self.cpu_registers.SP += 2

    def increment_PC(self, rel_addr):
        self.cpu_registers.PC += rel_addr

