codes = [0x2A, 0x2E, 0x3E, 0x26, 0x36]

def updateFlags(cpu, value: int):
  cpu.flags['c'] = value & 0b00000001
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x2A: # ROL A
      value = cpu.a
      cpu.a = (value << 1) | cpu.flags['c']
      cpu = updateFlags(cpu, cpu.a)
      cycles -= 1

    case 0x2E: # ROL abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value << 1) | cpu.flags['c'])
      cycles -= 5

    case 0x3E: # ROL abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value << 1) | cpu.flags['c'])
      cycles -= 6

    case 0x26: # ROL zero page
      address = cpu.ram.read(cpu.pc)
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value << 1) | cpu.flags['c'])
      cycles -= 4

    case 0x36: # ROL zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      value = cpu.ram.read(address)
      cpu.ram.write(address, (value << 1) | cpu.flags['c'])
      cycles -= 5

  cpu = updateFlags(cpu, cpu.ram.read(address))
  return cpu, cycles