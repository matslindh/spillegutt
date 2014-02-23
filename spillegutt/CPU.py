from Registers import CPURegisters, HardwareRegisters
from Memory import Memory
from functools import partial

class CPU:
    def __init__(self, cpu_registers, memory):
        self.cpu_registers = CPURegisters()
        self.hw_registers = HardwareRegisters()
        self.memory = Memory(self.hw_registers)
        self.reset()

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

            0x20: (1, self.instr_jr_nz),
            0x21: (1, self.instr_ld_hl),
            0x22: (1, self.instr_ldi_hli_a),
            0x23: (1, self.instr_inc_hl),
            0x24: (1, self.instr_inc_h),
            0x25: (1, self.instr_dec_h),
            0x26: (1, self.instr_ld_h),
            0x27: (1, self.instr_daa),
            0x28: (1, self.instr_jr_z),
            0x29: (1, self.instr_add_hl_hl),
            0x2A: (1, self.instr_ldi_a_hli),
            0x2B: (1, self.instr_dec_hl),
            0x2C: (1, self.instr_inc_l),
            0x2D: (1, self.instr_dec_l),
            0x2E: (1, self.instr_ld_l),
            0x2F: (1, self.instr_cpl),

            0x30: (1, self.instr_jr_nc),
            0x31: (1, self.instr_ld_sp),
            0x32: (1, self.instr_ldd_hli_a),
            0x33: (1, self.instr_inc_sp),
            0x34: (1, self.instr_inc_hli),
            0x35: (1, self.instr_dec_hli),
            0x36: (1, self.instr_ld_hli),
            0x37: (1, self.instr_scf),
            0x38: (1, self.instr_jr_c),
            0x39: (1, self.instr_add_hl_sp),
            0x3A: (1, self.instr_ldd_a_hli),
            0x3B: (1, self.instr_dec_sp),
            0x3C: (1, self.instr_inc_a),
            0x3D: (1, self.instr_dec_a),
            0x3E: (1, self.instr_ld_a),
            0x3F: (1, self.instr_ccf),
            
        }

    def reset(self):
        self.cpu_registers.AF = 0x01B0
        self.cpu_registers.BC = 0x0013
        self.cpu_registers.DE = 0x00D8
        self.cpu_registers.HL = 0x014D
        self.cpu_registers.SP = 0xFFFE
        self.cpu_registers.PC = 0x0100

        self.memory.write(0xFF05, 0x00)
        self.memory.write(0xFF06, 0x00)
        self.memory.write(0xFF07, 0x00)
        self.memory.write(0xFF10, 0x80)
        self.memory.write(0xFF11, 0xBF)
        self.memory.write(0xFF12, 0xF3)
        self.memory.write(0xFF14, 0xBF)
        self.memory.write(0xFF16, 0x3F)
        self.memory.write(0xFF17, 0x00)
        self.memory.write(0xFF19, 0xBF)
        self.memory.write(0xFF1A, 0x7F)
        self.memory.write(0xFF1B, 0xFF)
        self.memory.write(0xFF1C, 0x9F)
        self.memory.write(0xFF1E, 0xBF)
        self.memory.write(0xFF20, 0xFF)
        self.memory.write(0xFF21, 0x00)
        self.memory.write(0xFF22, 0x00)
        self.memory.write(0xFF23, 0xBF)
        self.memory.write(0xFF24, 0x77)
        self.memory.write(0xFF25, 0xF3)
        self.memory.write(0xFF26, 0xF1)
        self.memory.write(0xFF40, 0x91)
        self.memory.write(0xFF42, 0x00)
        self.memory.write(0xFF43, 0x00)
        self.memory.write(0xFF45, 0x00)
        self.memory.write(0xFF47, 0xFC)
        self.memory.write(0xFF48, 0xFF)
        self.memory.write(0xFF49, 0xFF)
        self.memory.write(0xFF4A, 0x00)
        self.memory.write(0xFF4B, 0x00)
        self.memory.write(0xFFFF, 0x00)

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
        self.cpu_registers.BC = self.inc_16b_set_flags(self.cpu_registers.BC)

    def instr_inc_b(self):
        self.cpu_registers.B = self.inc_8b_set_flags(self.cpu_registers.B)

    def instr_dec_b(self):
        self.cpu_registers.B = self.dec_8b_set_flags(self.cpu_registers.B)

    def instr_ld_b(self):
        self.cpu_registers.B = self.get_8b_from_PC()

    def instr_rlc_c(self):
        self.cpu_registers.C = self.rlc(self.cpu_registers.C)

    def instr_ld_nn_sp(self):
        self.memory[self.get_16b_from_PC()] = self.stack.pop()

    def instr_add_hl_bc(self):
        self.cpu_registers.HL = self.add_16b_set_flags(self.cpu_registers.HL, self.cpu_registers.BC)

    def instr_ld_a_bci(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.BC]

    def instr_dec_bc(self):
        self.cpu_registers.BC = self.dec_16b_set_flags(self.cpu_registers.BC)
        pass

    def instr_inc_c(self):
        self.cpu_registers.C = self.inc_8b_set_flags(self.cpu_registers.C)

    def instr_dec_c(self):
        self.cpu_registers.C = self.dec_8b_set_flags(self.cpu_registers.C)

    def instr_ld_c(self):
        self.cpu_registers.C = self.get_8b_from_PC()

    def instr_rrc_a(self):
        self.cpu_registers.A = self.rrc(self.cpu_registers.A)

    def instr_stop(self):
        # wait until p1-p10 go high
        # we have no concept of pins just yet
        pass

    def instr_ld_de(self):
        self.cpu_registers.BC = self.get_16b_from_PC()

    def instr_ld_dei_a(self):
        self.memory[self.cpu_registers.DE] = self.cpu_registers.A

    def instr_inc_de(self):
        self.cpu_registers.DE = self.inc_16b_set_flags(self.cpu_registers.DE)

    def instr_inc_d(self):
        self.cpu_registers.D = self.inc_8b_set_flags(self.cpu_registers.D)

    def instr_dec_d(self):
        self.cpu_registers.D = self.dec_8b_set_flags(self.cpu_registers.D)

    def instr_ld_d(self):
        self.cpu_registers.D = self.get_8b_from_PC()

    def instr_rl_a(self):
        self.cpu_registers.A = self.rl(self.cpu_registers.A)

    def instr_jr(self):
        # this might lead to us incrementing PC to get the value of the next bits
        # and then fubaring the relative jump. Will fix when we test.
        self.increment_PC(self.get_8b_from_PC())

    def instr_jr_c(self):
        if self.cpu_registers.flag(self.cpu_registers.FLAG_CARRY):
            self.increment_PC(self.get_8b_from_PC())

    def instr_jr_nc(self):
        if not self.cpu_registers.flag(self.cpu_registers.FLAG_CARRY):
            self.increment_PC(self.get_8b_from_PC())

    def instr_jr_nz(self):
        if not self.cpu_registers.flag(self.cpu_registers.FLAG_ZERO):
            self.increment_PC(self.get_8b_from_PC())

    def instr_jr_z(self):
        if self.cpu_registers.flag(self.cpu_registers.FLAG_ZERO):
            self.increment_PC(self.get_8b_from_PC())

    def instr_add_hl_de(self):
        self.cpu_registers.HL = self.add_16b_set_flags(self.cpu_registers.HL, self.cpu_registers.DE)

    def instr_ld_a_dei(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.DE]

    def instr_dec_de(self):
        self.cpu_registers.DE = self.dec_16b_set_flags(self.cpu_registers.DE)

    def instr_inc_e(self):
        self.cpu_registers.E = self.inc_8b_set_flags(self.cpu_registers.E)

    def instr_dec_e(self):
        self.cpu_registers.E = self.dec_8b_set_flags(self.cpu_registers.E)

    def instr_ld_e(self):
        self.cpu_registers.E = self.get_8b_from_PC()

    def instr_rr_a(self):
        self.cpu_registers.A = self.rr(self.cpu_registers.A)        

    def instr_ld_hl(self):
        self.cpu_registers.HL = self.get_16b_from_PC()

    def instr_ldi_hli_a(self):
        self.memory[self.cpu_registers.HL] = self.cpu_registers.A
        self.cpu_registers.HL = (self.cpu_registers.HL + 1)%65535

    def instr_inc_h(self):
        self.cpu_registers.H = self.inc_8b_set_flags(self.cpu_registers.H)

    def instr_dec_h(self):
        self.cpu_registers.H = self.dec_8b_set_flags(self.cpu_registers.H)

    def instr_ld_h(self):
        self.cpu_registers.H = self.get_8b_from_PC()

    def instr_daa(self):
        pass

    def instr_add_hl_hl(self):
        self.cpu_registers.HL = self.add_16b_set_flags(self.cpu_registers.HL, self.cpu_registers.HL)

    def instr_ldi_a_hli(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.HL]
        self.cpu_registers.HL = (self.cpu_registers.HL + 1) & 65535

    def instr_dec_hl(self):
        self.cpu_registers.HL = self.dec_16b_set_flags(self.cpu_registers.HL)

    def instr_inc_l(self):
        self.cpu_registers.L = self.inc_8b_set_flags(self.cpu_registers.L)

    def instr_dec_l(self):
        self.cpu_registers.L = self.dec_8b_set_flags(self.cpu_registers.L)

    def instr_ld_l(self):
        self.cpu_registers.L = self.get_8b_from_PC()

    def instr_cpl(self):
        self.cpu_registers.A = (~self.cpu_registers.A) & 127
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, True)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, True)

    def instr_inc_hl(self):
        self.cpu_registers.HL = self.inc_16b_set_flags(self.cpu_registers.HL)

    def instr_ld_sp(self):
        self.cpu_registers.SP = self.get_16b_from_PC()

    def instr_ldd_hli_a(self):
        self.memory[self.cpu_registers.HL] = self.cpu_registers.A
        self.cpu_registers.HL = (self.cpu_registers.HL - 1) % 65536

    def instr_inc_sp(self):
        self.cpu_registers.SP = self.inc_16b_set_flags(self.cpu_registers.SP)

    def instr_inc_hli(self):
        self.memory[self.cpu_registers.HL] = self.inc_8b_set_flags(self.memory[self.cpu_registers.HL])

    def instr_dec_hli(self):
        self.memory[self.cpu_registers.HL] = self.dec_8b_set_flags(self.memory[self.cpu_registers.HL])

    def instr_ld_hli(self):
        self.memory[self.cpu_registers.HL] = self.get_8b_from_PC()

    def instr_scf(self):
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, True)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, False)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, False)

    def instr_add_hl_sp(self):
        self.cpu_registers.HL = self.add_16b_set_flags(self.cpu_registers.HL, self.cpu_registers.SP)

    def instr_ldd_a_hli(self):
        self.cpu_registers.A = self.memory[self.cpu_registers.HL]]
        self.cpu_registers.HL = (self.cpu_registers.HL - 1) % 65536

    def instr_dec_sp(self):
        self.cpu_registers.SP = self.dec_16b_set_flags(self.cpu_registers.SP)

    def instr_inc_a(self):
        self.cpu_registers.A = self.inc_8b_set_flags(self.cpu_registers.A)

    def instr_dec_a(self):
        self.cpu_registers.A = self.dec_8b_set_flags(self.cpu_registers.A)

    def instr_ld_a(self):
        self.cpu_registers.A = self.get_8b_from_PC()

    def instr_ccf(self):
        pass

    def rl(self, value):
        flag = self.cpu_registers.flag(self.cpu_registers.FLAG_CARRY)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, value & 1)
        return ((value << 1)&127) | flag

    def rlc(self, value):
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, value & 128)
        return value << 1 + ((value & 128) >> 7)

    def rr(self, value):
        flag = self.cpu_registers.flag(self.cpu_registers.FLAG_CARRY)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, value & 1)
        return (value >> 1) | (flag << 7)

    def rrc(self, value):
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, value & 1)
        return value >> 1 + ((value & 1) << 7)

    def add_8b_set_flags(self, value, value2):
        new_val = value + value2

        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, False)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, new_val&256)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_ZERO, new_val == 0)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, (value&0xf + value2&0xf)&0x10)

        return new_val & 255

    def add_16b_set_flags(self, value, value2):
        new_val = value + value2

        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, False)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, new_val & 65536)
        #self.cpu_registers.set_flag(self.cpu_registers.FLAG_ZERO, new_val == 0)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, (value&0xfff + value&0xfff)&0x1000)
        
        return new_val & 65535

    def inc_8b_set_flags(self, value):
        new_val = value + 1

        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, False)
        #self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, new_val&256)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_ZERO, new_val == 0)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, (new_val&0xf + value&0xf)&0x10)
        
        return new_val & 255

    def inc_16b_set_flags(self, value):
        return (value+1)&65535

    def sub_8b_set_flags(self, value, value2):
        new_val = value + value2

        self.cpu_registers.set_flag(self.cpu_registers.FLAG_SUBTRACT, False)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_CARRY, new_val&256)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_ZERO, new_val == 0)
        self.cpu_registers.set_flag(self.cpu_registers.FLAG_HALF_CARRY, (value&0xf + value&0xf)&0x10)

        return new_val & 255

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

