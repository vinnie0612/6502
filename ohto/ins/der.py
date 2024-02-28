m_codes = [0xCE, 0xDE, 0xC6, 0xD6]
x_code = 0xCA
y_code = 0x88
codes = [x_code, y_code] + m_codes

def updateFlags(cpu, value: int):
  cpu.flags['z'] = value == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0xCA: # DEX
      cpu.x -= 1
      cycles -= 1

    case 0x88: # DEY
      cpu.y -= 1
      cycles -= 1

    case 0xCE: # DEC abs
      address = cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)
      value = cpu.ram.read(address) - 1
      cpu.ram.write(address, value)
      cycles -= 5

    case 0xDE: # DEC abs, X
      address = (cpu.ram.read(cpu.pc) | (cpu.ram.read(cpu.pc+1) << 8)) + cpu.x
      value = cpu.ram.read(address) - 1
      cpu.ram.write(address, value)
      cycles -= 6

    case 0xC6: # DEC zero page
      address = cpu.ram.read(cpu.pc)
      value = cpu.ram.read(address) - 1
      cpu.ram.write(address, value)
      cycles -= 4

    case 0xD6: # DEC zero page, X
      address = cpu.ram.read(cpu.pc) + cpu.x
      value = cpu.ram.read(address) - 1
      cpu.ram.write(address, value)
      cycles -= 5

  cpu = updateFlags(cpu, value)
  return cpu, cycles