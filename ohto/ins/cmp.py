codes = [0xC9, 0xCD, 0xDD, 0xD9, 0xC5, 0xD5, 0xC1, 0xD1]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = value & 0x80 > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0xC9: # CMP immediate
      value = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 1

    case 0xCD: # CMP absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 3

    case 0xDD: # CMP absolute, X
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.x)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 3

    case 0xD9: # CMP absolute, Y
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.y)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 3

    case 0xC5: # CMP zero page
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 2

    case 0xD5: # CMP zero page, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read((address + cpu.x) & 0xFF)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 3

    case 0xC1: # CMP indirect, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read((address + cpu.x) & 0xFF)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 5

    case 0xD1: # CMP indirect, Y
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      result = cpu.a - value
      cpu.flags['c'] = cpu.a >= value
      updateFlags(cpu, result)
      cycles -= 4

  return cpu, cycles