#!/usr/bin/env python3
# Author: Bryan Cain
# Date: December 31, 2010
# Description: Attempts to restore the original sound samples to SNES ROMs in 
# 	Virtual Console games, which use uncompressed PCM data separate from the ROM.
# Ported/slightly modified to python3 by Minxrod

import os
import sys
import struct
from brrencode3 import BRREncoder
from io import BytesIO

# vcrom: file-like object for the original VC ROM
# brr: file-like object containing the BRR-compressed audio samples
# Precondition: brr is the correct size
def restore_brr_samples(vcrom, pcm):
	# read the samples from the input ROM into memory (TODO: check file size first)
	vcrom.seek(0)
	str = vcrom.read()
	samplestart = str.find(b'PCMF') # samples start with first instance of the string "PCMF"
	str = str[samplestart:]
	
	# initialize output ROM in memory as a StringIO (pseudo-file)
	rom = BytesIO()
	rom.write(str)
	
	# read the input BRR samples
	#brr.seek(0)
	#brrdata = brr.read()
	#lastbrroffset = None
	
	enc = BRREncoder(pcm, None)
	lastpcmoffset = 0
	
	# misc. variables
	#goodrom = open('SNADNE1.667', 'rb')
	wrong = 0
	controlwrong = 0
	indices = []
	
	while str.find(b'PCMF') >= 0:
		index = str.find(b'PCMF')
		filepos = samplestart + index
		
		# error checking to prevent infinite loops
		#assert index not in indices
		#indices.append(index)
		
		pcmf, pcmoffset = struct.unpack('<4sI', str[index:index+8])
		pcmoffset &= 0xffffff
		if pcmoffset % 16 or pcmoffset < lastpcmoffset:
			#print '%08x: unexpected offset %d' % (filepos, pcmoffset)
			pcmoffset = lastpcmoffset + 16
		#else:
		#	brroffset = 9 * (brroffset >> 4)
		
		# read the BRR sample
		#brr.seek(brroffset)
		#brrsample = brr.read(9)
		
		# read and encode the BRR block
		brrsample = enc.encode_block(pcmoffset)
		
		# error checking for invalid BRR offsets
		if len(brrsample) != 9:
			raise ValueError('Invalid BRR offset: %d' % brroffset)
		
		# set the END bit in the BRR sample if it is set in the PCMF block
		if str[index+7] & 1:
			brrsample = bytes([brrsample[0] | 1]) + brrsample[1:]
		
		# set the LOOP bit in the BRR sample if it is set in the PCMF block
		if str[index+7] & 2:
			brrsample = bytes([brrsample[0] | 2]) + brrsample[1:]
		
		# checks whether sample matches the original ROM, when the original ROM is available (for debugging purposes)
		'''goodrom.seek(samplestart + index)
		grsample = goodrom.read(9)
		if brrsample != grsample:
			wrong += 1
			sys.stdout.write('%08x: ' % filepos)
			#if brrdata.find(grsample) >= 0:
			#	print 'wrong sample, correct BRR offset is %08x' % brrdata.find(grsample)
			if brrsample[1:] == grsample[1:]:
				if abs(ord(brrsample[0]) - ord(grsample[0])) <= 3:
					controlwrong += 1
					print 'SPC700 control bits differ'
				else:
					print 'flags are different'
			else:
				print 'sample encoded differently?' '''
		
		rom.seek(index)
		rom.write(brrsample)
		str = rom.getvalue()
		lastpcmoffset = pcmoffset
	
	#print '%d wrong samples' % wrong
	#print '%d differences in SPC700 control bits' % controlwrong
	
	rom.close()
	vcrom.seek(0)
	return vcrom.read(samplestart) + str

def restore(rom_name = "snes.rom", pcm_name = "snes.pcm", out_name = "snes.out"):
	import time
	
	vcrom = open(rom_name, 'rb')
	pcm = open(pcm_name, 'rb')
	
	'''# encode raw PCM in SNES BRR format
	print 'Encoding audio as BRR'
	brr = StringIO()
	enc = BRREncoder(pcm, brr)
	enc.encode()
	pcm.close()'''
	
	# encode and inject BRR sound data into the ROM
	print('Encoding and restoring BRR audio data to ROM')
	start = time.perf_counter()
	string = restore_brr_samples(vcrom, pcm)
	end = time.perf_counter()
	print('Time: %.2f seconds' % (end - start))
	
	# write to file
	output = open(out_name, "wb")
	output.write(string)
	output.close()
	pcm.close()
	#print 'done'

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print('Usage: snesrestore game.rom game.pcm output.smc')
		sys.exit(1)
	
	restore(*sys.argv)