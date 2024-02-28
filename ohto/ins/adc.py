codes = [0x69, 0x6D, 0x7D, 0x79, 0x65, 0x75, 0x61, 0x71]

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x69: # ADC immediate
      value = cpu.ram.read(cpu.pc)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 1

    case 0x6D: # ADC absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 3

    case 0x7D: # ADC absolute, X
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.x)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 3

    case 0x79: # ADC absolute, Y
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      value = cpu.ram.read(address + cpu.y)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 3

    case 0x65: # ADC zero page
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 2

    case 0x75: # ADC zero page, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(address + cpu.x)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 2

    case 0x61: # ADC indirect, X
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(cpu.ram.read16(address + cpu.x))
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 2

    case 0x71: # ADC indirect, Y
      address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      value = cpu.ram.read(cpu.ram.read16(address) + cpu.y)
      cpu.a += value
      cpu.a += int(cpu.flags['c'])
      cpu.flags['c'] = cpu.a > 0xFF
      cpu.flags['v'] = (cpu.a ^ value) & (cpu.a ^ cpu.a) & 0x80
      cpu.a &= 0xFF
      updateFlags(cpu, cpu.a)
      cycles -= 2

  return cpu, cycles
