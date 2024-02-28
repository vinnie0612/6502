from ram import RAM
from cpu import CPU

def main():
  ram = RAM(64 * 1024)
  cpu = CPU(ram)

  cpu.reset()
  ram.initialize_from_binary("rom.bin")

  cpu.execute(300)

if __name__ == "__main__":
  main()