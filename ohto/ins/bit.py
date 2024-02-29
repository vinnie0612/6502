codes = [0x2C, 0x24]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['v'] = (value & 0b01000000) > 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x2C: # BIT abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      value = cpu.ram.read(address)
      cpu.flags['z'] = (cpu.a & value) == 0
      cpu.flags['v'] = (value & 0b01000000) > 0
      cpu.flags['n'] = (value & 0b10000000) > 0
      cycles -= 3
      cpu.pc += 2

    case 0x24: # BIT zero page
      address = cpu.ram.read(cpu.pc)
      value = cpu.ram.read(address)
      cpu.flags['z'] = (cpu.a & value) == 0
      cpu.flags['v'] = (value & 0b01000000) > 0
      cpu.flags['n'] = (value & 0b10000000) > 0
      cycles -= 2

  return cpu, cycles