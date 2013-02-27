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

            0x10: (1, self.instr_stop),
            0x11: (1, self.instr_ld_de),
            0x12: (1, self.instr_ld_dei_a),
            0x13: (1, self.instr_ld_inc_de),
            0x14: (1, self.instr_ld_inc_d),
            0x15: (1, self.instr_dec_d),
            0x16: (1, self.instr_ld_d),
            0x17: (1, self.instr_rl_a),
            0x18: (1, self.instr_jr),
            0x19: (1, self.instr_add_hl_de),
            0x1A: (1, self.instr_ld_a_dei),
            0x1B: (1, self.instr_dec_de),
            0x1C: (1, self.instr_inc_e),
            0x1D: (1, self.instr_dec_e),
            0x1E: (1, self.instr_ld_e),
            0x1F: (1, self.instr_rr_a),
        }

    def execute(self):
        cycles, instr = self.ops[self.get_8b_from_PC()]
        instr()

    def instr_nop(self):
        return

    def instr_ld_bc(self):
        self.cpu_registers.BC = self.get_16b_from_PC()

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

    def instr_add_hl_bc(self):
        self.cpu_registers.HL = self.cpu_registers.HL + self.cpu_registers.BC

    def instr_ld_a_bci(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.BC]

    def instr_dec_bc(self):
        self.cpu_registers.BC = self.cpu_registers.BC - 1
        pass

    def instr_inc_c(self):
        self.cpu_registers.C += 1

    def instr_dec_c(self):
        self.cpu_registers.C -= 1

    def instr_ld_c(self):
        self.cpu_registers.C = self.get_8b_from_PC()

    def instr_rrc_a(self):
        self.cpu_registers.A = self.rrc_it(self.cpu_registers.A)

    def instr_stop(self):
        # wait until p1-p10 go high
        # we have no concept of pins just yet
        pass

    def instr_ld_de(self):
        self.cpu_registers.BC = self.get_16b_from_PC()

    def instr_ld_dei_a(self):
        self.memory[self.cpu_registers.DE] = self.cpu_registers.A

    def instr_inc_de(self):
        self.cpu_registers.DE += 1

    def instr_inc_d(self):
        self.cpu_registers.D += 1

    def instr_dec_d(self):
        self.cpu_registers.D -= 1

    def instr_ld_d(self):
        self.cpu_registers.D = self.get_8b_from_PC()

    def instr_rl_a(self):
        pass

    def instr_jr(self):
        # this might lead to us incrementing PC to get the value of the next bits
        # and then fubaring the relative jump. Will fix when we test.
        self.increment_PC(self.get_8b_from_PC())

    def instr_add_hl_de(self):
        self.cpu_registers.HL += self.cpu_registers.DE

    def instr_ld_a_dei(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.DE]

    def instr_dec_de(self):
        self.cpu_registers.DE -= 1

    def instr_inc_e(self):
        self.cpu_registers.E += 1

    def instr_dec_e(self):
        self.cpu_registers.E -= 1

    def instr_ld_e(self):
        self.cpu_registers.E = self.get_8b_from_PC()

    def instr_rr_a(self):
        pass

    def rlc_it(self, value):
        if value & 128:
            self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY)
        else:
            self.cpu_registers.reset_flag(self.cpu_registers.FLAG_CARRY)

        return value << 1 + ((value & 128) >> 7)

    def rrc_it(self, value):
        if value & 1:
            self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY)
        else:
            self.cpu_registers.reset_flag(self.cpu_registers.FLAG_CARRY)

        return value >> 1 + ((value & 1) << 7)

    def get_8b_from_PC(self):
        val = self.memory[self.cpu_registers.PC]
        self.increment_PC(1)

        return val

    def get_16b_from_PC(self):
        val = self.memory[self.cpu_registers.PC] << 8 + self.memory[self.cpu_registers.PC+1]
        self.increment_PC(2)

        return val

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

