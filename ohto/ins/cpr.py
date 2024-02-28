cpx_codes = [0xE0, 0xE4, 0xEC]
cpy_codes = [0xC0, 0xC4, 0xCC]
codes = cpx_codes + cpy_codes

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = value & 0x80 > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0xE0: # CPX immediate
      value = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      result = cpu.x - value
      cpu.flags['c'] = cpu.x >= value
      updateFlags(cpu, result)
      cycles -= 1

    case 0xE4: # CPX zero page
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      result = cpu.x - value
      cpu.flags['c'] = cpu.x >= value
      updateFlags(cpu, result)
      cycles -= 2

    case 0xEC: # CPX absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address)
      result = cpu.x - value
      cpu.flags['c'] = cpu.x >= value
      updateFlags(cpu, result)
      cycles -= 3

    case 0xC0: # CPY immediate
      value = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      result = cpu.y - value
      cpu.flags['c'] = cpu.y >= value
      updateFlags(cpu, result)
      cycles -= 1

    case 0xC4: # CPY zero page
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      result = cpu.y - value
      cpu.flags['c'] = cpu.y >= value
      updateFlags(cpu, result)
      cycles -= 2

    case 0xCC: # CPY absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address)
      result = cpu.y - value
      cpu.flags['c'] = cpu.y >= value
      updateFlags(cpu, result)
      cycles -= 3

  return cpu, cycles