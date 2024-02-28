all:
	./vasm/vasm6502_oldstyle -Fbin -dotdir -o main.bin main.asm
	mv main.bin ohto/rom.bin
	cd ohto && python main.py