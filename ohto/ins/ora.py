codes = [0x09, 0x0D, 0x1D, 0x19, 0x05, 0x15, 0x01, 0x11]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x09: # ORA #
      cpu.a |= cpu.ram.read(cpu.pc)
      cycles -= 1

    case 0x0D: # ORA abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      cpu.a |= cpu.ram.read(address)
      cycles -= 3

    case 0x1D: # ORA abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      cpu.a |= cpu.ram.read(address)
      cycles -= 3

    case 0x19: # ORA abs, Y
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.y
      cpu.a |= cpu.ram.read(address)
      cycles -= 3

    case 0x05: # ORA zero page
      address = cpu.ram.read(cpu.pc)
      cpu.a |= cpu.ram.read(address)
      cycles -= 2

    case 0x15: # ORA zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      cpu.a |= cpu.ram.read(address)
      cycles -= 3

    case 0x01: # ORA (indirect, X)
      address = cpu.ram.read(cpu.pc) + cpu.x
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8)
      cpu.a |= cpu.ram.read(address)
      cycles -= 5

    case 0x11: # ORA (indirect), Y
      address = cpu.ram.read(cpu.pc)
      address = cpu.ram.read(address) | (cpu.ram.read(address+1) << 8) + cpu.y
      cpu.a |= cpu.ram.read(address)
      cycles -= 4

  cpu = updateFlags(cpu, cpu.a)
  return cpu, cycles