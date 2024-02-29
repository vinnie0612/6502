m_codes = [0xEE, 0xFE, 0xE6, 0xF6]
x_code = 0xE8
y_code = 0xC8
codes = [x_code, y_code] + m_codes

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  value = 0
  match opcode:
    case 0xE8: # INX
      cpu.x += 1
      cycles -= 1

    case 0xC8: # INY
      cpu.y += 1
      cycles -= 1

    case 0xEE: # INC abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      value = cpu.ram.read(address) + 1
      cpu.ram.write(address, value)
      cycles -= 5

    case 0xFE: # INC abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      value = cpu.ram.read(address) + 1
      cpu.ram.write(address, value)
      cycles -= 6

    case 0xE6: # INC zero page
      address = cpu.ram.read(cpu.pc)
      value = cpu.ram.read(address) + 1
      cpu.ram.write(address, value)
      cycles -= 4

    case 0xF6: # INC zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      value = cpu.ram.read(address) + 1
      cpu.ram.write(address, value)
      cycles -= 5

  if value:
    cpu = updateFlags(cpu, value)
  return cpu, cycles