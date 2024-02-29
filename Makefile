all:
	./vasm/vasm6502_oldstyle -Fbin -dotdir -o main.bin main.asm
	mv main.bin ohto/rom.bin
	cd ohto && python3 main.py

rom: 
	./vasm/vasm6502_oldstyle -Fbin -dotdir -o main.bin main.asm
	mv main.bin ohto/rom.bin
	hexdump -C ohto/rom.bin
