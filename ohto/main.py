from ram import RAM
from cpu import CPU

def main():
  ram = RAM(64 * 1024)
  cpu = CPU(ram, singleStep=False, delay=0.03, debug=True)

  ram.initialize_from_binary("rom.bin")
  cpu.reset()

  cpu.execute(forever=True)

if __name__ == "__main__":
  main()
