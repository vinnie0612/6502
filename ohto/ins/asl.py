codes = [0x0A, 0x0E, 0x1E, 0x06, 0x16]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  cpu.flags['c'] = (value & 0b100000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x0A: # ASL A
      cpu.a = (cpu.a << 1) & 0xFF
      cpu = updateFlags(cpu, cpu.a)
      cycles -= 1
    case 0x0E: # ASL abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      cpu.ram.write(address, (cpu.ram.read(address) << 1) & 0xFF)
      cycles -= 5
    case 0x1E: # ASL abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      cpu.ram.write(address, (cpu.ram.read(address) << 1) & 0xFF)
      cycles -= 6
    case 0x06: # ASL zero page
      address = cpu.ram.read(cpu.pc)
      cpu.ram.write(address, (cpu.ram.read(address) << 1) & 0xFF)
      cycles -= 4
    case 0x16: # ASL zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      cpu.ram.write(address, (cpu.ram.read(address) << 1) & 0xFF)
      cycles -= 5

  cpu = updateFlags(cpu, cpu.ram.read(address))
  return cpu, cycles