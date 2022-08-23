import sys

def trim_and_pad(filename = "snes.out", fixed = None):
	"""
	Removes the header that snesrestore creates and pads the rom to the nearest 256 bytes 
	To be honest, I don't know why the padding is needed, but it made Super Mario Kart playable.
	Checksum is bad according to snes9x, but it plays.
	"""
	with open(filename, "rb") as f:
		_ = f.read(0x24)  # discard
		data = f.read()
		while len(data) % 256 != 0:
			data += b'\xff'
		with open(fixed if fixed else "fixed-"+filename, "wb") as out:
			out.write(data)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("badtosfc.py <snesrestore.py output> [output filename]")
		sys.exit(0)
	trim_and_pad(*sys.argv)
	