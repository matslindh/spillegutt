def asciify(b):
	s = b.decode("ascii")
	return s.strip().strip("\x00")

def romtypify(id):
	return Loader.cartridge_types[ord(id)]

class Loader:
	meta_information = {
		'entry_point': (0x100, 0x103),
		'nintendo_logo': (0x104, 0x133),
		'title': (0x134, 0x143, asciify),
		'manufacturer_code_modern': (0x13f, 0x142, asciify),
		'cgb_flag': (0x143, 0x143),
		'license_code_modern': (0x144, 0x145),
		'sgb_flag': (0x146, 0x146),
		'cartridge_type': (0x147, 0x147, romtypify),
		'rom_size': (0x148, 0x148),
		'ram_size': (0x149, 0x149),
		'destination_code': (0x14a, 0x14a),
		'license_code_old': (0x14b, 0x14b),
		'version_number': (0x14c, 0x14c),
		'checksum': (0x14d, 0x14d),
		'checksum_global': (0x14e, 0x14f),
	}

	INVALID = -1
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

	cartridge_types = {
		0x00: ROM_ONLY,
		0x01: MBC1,
		0x02: MBC1 | RAM,
		0x03: MBC1 | RAM | BATTERY,
		0x04: INVALID,
		0x05: MBC2,
		0x06: MBC2 | BATTERY,
		0x07: INVALID,
		0x08: RAM,
		0x09: RAM | BATTERY,
		0x0A: INVALID,
		0x0B: MMM01,
		0x0C: MMM01 | RAM,
		0x0D: MMM01 | RAM | BATTERY,
		0x0E: INVALID,
		0x0F: MBC3 | TIMER | BATTERY,
		0x10: MBC3 | TIMER | RAM | BATTERY,
		0x11: MBC3,
		0x12: MBC3 | RAM,
		0x13: MBC3 | RAM | BATTERY,
		0x14: INVALID,
		0x15: MBC4,
		0x16: MBC4 | RAM,
		0x17: MBC4 | RAM | BATTERY,
		0x18: INVALID,
		0x19: MBC5,
		0x1A: MBC5 | RAM,
		0x1B: MBC5 | RAM | BATTERY,
		0x1C: MBC5 | RUMBLE,
		0x1D: MBC5 | RUMBLE | RAM,
		0x1E: MBC5 | RUMBLE | RAM | BATTERY,
		0x1F: INVALID,
	}

	nintendo_logo = b'\xCE\xED\x66\x66\xCC\x0D\x00\x0B\x03\x73\x00\x83\x00\x0C\x00\x0D\x00\x08\x11\x1F\x88\x89\x00\x0E\xDC\xCC\x6E\xE6\xDD\xDD\xD9\x99\xBB\xBB\x67\x63\x6E\x0E\xEC\xCC\xDD\xDC\x99\x9F\xBB\xB9\x33\x3E'

	def __init__(self, memory):
		self.memory = memory
		self.last_error_msg = None
		self.meta_loaded = None

	def load(self, path):
		self.path = path
		self.memory.load(open(self.path, "rb").read())

		meta = self.meta()

		return self.is_valid()

	def is_valid(self):
		data = self.memory.dump()
		meta = self.meta()

		if self.checksum_8b(data[0x134:0x14d]) != ord(meta['checksum']):
			self.last_error_msg = "Wrong header checksum."
			return None

		if self.checksum_16b(data) != self.bytearray_to_16b(meta['checksum_global']):
			self.last_error_msg = "Wrong global checksum."
			return None

		if meta['nintendo_logo'] != self.nintendo_logo:
			self.last_error_msg = "Nintendo logo not present in file."
			return None

		return True

	def last_error(self):
		return self.last_error_msg

	def meta(self):
		if self.meta_loaded:
			return self.meta_loaded

		data = self.memory.dump()
		meta = {}

		for entry in self.meta_information:
			spec = self.meta_information[entry]
			value = data[spec[0]:spec[1]+1]

			if len(spec) > 2:
				value = spec[2](value)

			meta[entry] = value

		self.meta_loaded = meta
		return meta

	def checksum_8b(self, data):
		checksum = 0

		for byte in data:
			checksum = (checksum - byte - 1)%256

		return checksum

	def checksum_16b(self, data):
		data = data[:0x14e] + data[0x150:]
		checksum = 0

		for byte in data:
			checksum = (checksum + byte) % 65536

		return checksum

	def bytearray_to_16b(self, data):
		return (data[0] << 8) + data[1]