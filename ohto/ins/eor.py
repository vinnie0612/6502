codes = [0x49, 0x4D, 0x5D, 0x59, 0x45, 0x55, 0x41, 0x51]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x49: # EOR #
      cpu.a ^= cpu.ram.read(cpu.pc)
      cycles -= 1

    case 0x4D: # EOR abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      cpu.a ^= cpu.ram.read(address)
      cycles -= 3

    case 0x5D: # EOR abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      cpu.a ^= cpu.ram.read(address)
      cycles -= 3

    case 0x59: # EOR abs, Y
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.y
      cpu.a ^= cpu.ram.read(address)
      cycles -= 3

    case 0x45: # EOR zero page
      address = cpu.ram.read(cpu.pc)
      cpu.a ^= cpu.ram.read(address)
      cycles -= 2

    case 0x55: # EOR zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      cpu.a ^= cpu.ram.read(address)
      cycles -= 2

    case 0x41: # EOR (indirect, X)
      address = cpu.ram.read(cpu.pc) + cpu.x
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8)
      cpu.a ^= cpu.ram.read(address)
      cycles -= 2

    case 0x51: # EOR (indirect), Y
      address = cpu.ram.read(cpu.pc)
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8) + cpu.y
      cpu.a ^= cpu.ram.read(address)
      cycles -= 2

  cpu = updateFlags(cpu, cpu.a)
  return cpu, cycles