import sys

from datasplit import split
from badtosfc import trim_and_pad
from snesrestore import restore

if __name__ == "__main__":
	out_name = "snes.rom" if len(sys.argv) < 3 else sys.argv[2]
	if len(sys.argv) < 2:
		print("vc3dstosfc.py <data.bin path>")
	
	split(sys.argv[1])
	restore()
	trim_and_pad("snes.out", out_name)