
codes = [0x4A, 0x4E, 0x5E, 0x46, 0x56]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x4A: # LSR A
      cpu.flags['c'] = cpu.a & 0b00000001
      cpu.a = cpu.a >> 1
      cpu = updateFlags(cpu, cpu.a)
      cycles -= 1

    case 0x4E: # LSR abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      cpu.flags['c'] = cpu.ram.read(address) & 0b00000001
      cpu.ram.write(address, cpu.ram.read(address) >> 1)
      cycles -= 5

    case 0x5E: # LSR abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      cpu.flags['c'] = cpu.ram.read(address) & 0b00000001
      cpu.ram.write(address, cpu.ram.read(address) >> 1)
      cycles -= 6

    case 0x46: # LSR zero page
      address = cpu.ram.read(cpu.pc)
      cpu.flags['c'] = cpu.ram.read(address) & 0b00000001
      cpu.ram.write(address, cpu.ram.read(address) >> 1)
      cycles -= 4

    case 0x56: # LSR zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      cpu.flags['c'] = cpu.ram.read(address) & 0b00000001
      cpu.ram.write(address, cpu.ram.read(address) >> 1)
      cycles -= 5

  cpu = updateFlags(cpu, cpu.ram.read(address))
  return cpu, cycles