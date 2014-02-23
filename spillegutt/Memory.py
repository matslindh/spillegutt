class Memory:
    ROM_ONLY = 0
    MBC1 = 1
    MBC2 = 2
    MBC3 = 4
    MBC4 = 8
    MBC5 = 16
    RAM = 32
    BATTERY = 64
    TIMER = 128
    MMM01 = 256
    RUMBLE = 512

    ROM_BANKING = 0
    RAM_BANKING = 1

    def __init__(self, hw_registers):
        self.hw_registers = hw_registers
        self.memory = bytearray(65536)
        self.mode = Memory.ROM_ONLY
        self.bank_mode = Memory.ROM_BANKING
        self.rom_bank = 0
        self.ram_bank = 0
        self.ram_enabled = False

    def set_mode(self, mode):
        self.mode = mode

    def load(self, bytes_load):
        self.memory[0:len(self.memory)] = bytes_load

    def dump(self):
        return self.memory

    def write(self, addr, val):
        if addr < 0x8000:
            if self.mode & Memory.MBC1:
                if addr < 0x1fff:
                    if val & 0xA:
                        self.ram_enabled = True
                    else:
                        self.ram_enabled = False
                elif addr < 0x3fff:
                    self.rom_bank = val & 0x1F

                    if not self.rom_bank:
                        self.rom_bank = 1

                elif addr < 0x5fff:
                    if self.bank_mode == Memory.RAM_BANKING:
                        self.ram_bank = val & 3
                    elif self.bank_mode == Memory.ROM_BANKING:
                        self.rom_bank += (val & 3) << 5

                elif addr < 0x7fff:
                    if val:
                        self.bank_mode = Memory.RAM_BANKING
                    else:
                        self.bank_mode = Memory.ROM_BANKING
        elif self.ram_enabled:
            if self.mode & Memory.MBC1:
                if addr >= 0xA000 and addr < 0xc000:
                    l_addr = addr - 0xA000
                    self.ram_banks[self.ram_bank][l_addr] = val

    def read(self, addr):
        # might be fast enough to copy memory into the memory area instead on bank switch, and let us keep the logic simpler
        if self.mode & Memory.MBC1:
            if addr >= 0xA000 and addr < 0xc000:
                l_addr = addr - 0xA000
                return self.ram_banks[self.ram_bank][l_addr]

        return self.memory[addr]

    def get_16b(self, addr):
        return (self.memory[addr] << 8) + self.memory[addr+1]