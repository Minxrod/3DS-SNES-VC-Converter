import sys

def read_u24(slice):
	return slice[0] + slice[1] * 256 + slice[2] * 65536

def split(filename, romout="snes.rom", pcmout="snes.pcm"):
	"""
	Splits a 3DS SNES VC data.bin file into the PCM and ROM sections.
	Header is discarded and anything extra is ignored.
	"""
	with open(sys.argv[1],'rb') as f:
		head = f.read(60)
		rom_size = read_u24(head[0x31:0x34])
		pcm_size = read_u24(head[0x35:0x38])
		
		print(f"Rom size: {rom_size}")
		print(f"PCM size: {pcm_size}")
		rom = f.read(rom_size)
		pcm = f.read(pcm_size)
		
		with open(romout, "wb") as out:
			out.write(rom)
		with open(pcmout, "wb") as out:
			out.write(pcm)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("datasplit.py <data.bin path>")
		sys.exit(0)
	
	split(sys.argv[1])