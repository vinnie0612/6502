codes = [0x29, 0x2D, 0x3D, 0x39, 0x25, 0x35, 0x21, 0x31]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x29: # AND #
      cpu.a &= cpu.ram.read(cpu.pc)
      cycles -= 1

    case 0x2D: # AND abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      cpu.a &= cpu.ram.read(address)
      cycles -= 3

    case 0x3D: # AND abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      cpu.a &= cpu.ram.read(address)
      cycles -= 3

    case 0x39: # AND abs, Y
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.y
      cpu.a &= cpu.ram.read(address)
      cycles -= 3

    case 0x25: # AND zero page
      address = cpu.ram.read(cpu.pc)
      cpu.a &= cpu.ram.read(address)
      cycles -= 2

    case 0x35: # AND zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      cpu.a &= cpu.ram.read(address)
      cycles -= 2

    case 0x21: # AND (indirect, X)
      address = cpu.ram.read(cpu.pc) + cpu.x
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8)
      cpu.a &= cpu.ram.read(address)
      cycles -= 2

    case 0x31: # AND (indirect), Y
      address = cpu.ram.read(cpu.pc)
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8) + cpu.y
      cpu.a &= cpu.ram.read(address)
      cycles -= 2

  cpu = updateFlags(cpu, cpu.a)
  return cpu, cycles