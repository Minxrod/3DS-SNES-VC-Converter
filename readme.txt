About:
This is a collection of small wrapper scripts that, when used together, created SNES roms that worked in snes9x.

In this case, "worked" means that the game
* doesn't sound broken immediately
* works for about a minute without obvious problems

This might break completely, it's not well tested. This is built on top of snesrestore.py, from vcromclaim.
The additions just convert data.bin into a format usable by snesrestore, and then convert to .sfc format.

Usage:
Requires Python 3, only tested on Windows but probably works on other operating systems as well.
You must extract the data.bin from your virtual console title to use this tool. This can be done using GodMode9, or using Citra's "Dump RomFS" option.

python vc3dstosfc.py <path to data.bin> [output filename]

Games Tested:
* Super Mario World
* Super Mario Kart
* Kirby's Dream Course
* The Legend of Zelda: A Link to the Past
* Earthbound

Possible issues:
None of these games contained "SDD-1" graphics, so I don't know if this works with those games at all. (See linked 3dbrew page)

Useful links:
https://github.com/Plombo/vcromclaim
https://gbatemp.net/threads/extracting-snes-vc-rom-restoring-audio.583963/
https://www.3dbrew.org/wiki/3DS_Virtual_Console#SNES_VC