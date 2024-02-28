codes = [0x6A, 0x6E, 0x7E, 0x66, 0x76]

def updateFlags(cpu, value: int):
  cpu.flags['c'] = value & 0b10000000
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x6A: # ROR A
      value = cpu.a
      cpu.a = (value >> 1) | (cpu.flags['c'] << 7)
      cpu = updateFlags(cpu, cpu.a)
      cycles -= 1

    case 0x6E: # ROR abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value >> 1) | (cpu.flags['c'] << 7))
      cycles -= 5

    case 0x7E: # ROR abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value >> 1) | (cpu.flags['c'] << 7))
      cycles -= 6

    case 0x66: # ROR zero page
      address = cpu.ram.read(cpu.pc)
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value >> 1) | (cpu.flags['c'] << 7))
      cycles -= 4

    case 0x76: # ROR zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value >> 1) | (cpu.flags['c'] << 7))
      cycles -= 5

  cpu = updateFlags(cpu, cpu.ram.read(address))
  return cpu, cycles