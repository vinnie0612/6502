codes = [0xE9, 0xED, 0xFD, 0xF9, 0xE5, 0xF5, 0xE1, 0xF1]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = value & 0x80 > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0xE9: # SBC immediate
      value = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 1

    case 0xED: # SBC absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 3

    case 0xFD: # SBC absolute, X
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.x)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 3

    case 0xF9: # SBC absolute, Y
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.y)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 3

    case 0xE5: # SBC zero page
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 2

    case 0xF5: # SBC zero page, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address + cpu.x)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 3

    case 0xE1: # SBC indirect, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(cpu.ram.read16(address + cpu.x))
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 5

    case 0xF1: # SBC indirect, Y
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(cpu.ram.read16(address) + cpu.y)
      result = cpu.a - value - (1 - int(cpu.flags['c']))
      cpu.flags['c'] = result >= 0
      cpu.flags['v'] = (cpu.a ^ result) & (cpu.a ^ value) & 0x80 > 0
      updateFlags(cpu, result)
      cpu.a = result
      cycles -= 4

  return cpu, cycles
