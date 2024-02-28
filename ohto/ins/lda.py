codes = [0xA9, 0xA5, 0xB5, 0xAD, 0xBD, 0xB9]

def updateFlags(cpu, value: int) -> None:
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0xA9:  # LDA immediate
      cpu.a = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      cycles -= 1

    case 0xA5:  # LDA zero page
      zero_page_address = cpu.ram.read(cpu.pc)
      cycles -= 1
      cpu.a = cpu.ram.read(zero_page_address)
      cpu.pc += 1
      cycles -= 1

    case 0xB5:  # LDA zero page, X
      zero_page_address = (cpu.ram.read(cpu.pc) + cpu.x) & 0xFF
      cycles -= 2
      cpu.a = cpu.ram.read(zero_page_address)
      cpu.pc += 1
      cycles -= 1

    case 0xAD:  # LDA absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.a = cpu.ram.read(address)
      cycles -= 1

    case 0xBD: # LDA absolute, X
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.a = cpu.ram.read(address + cpu.x)
      cycles -= 1

    case 0xB9: # LDA absolute, Y
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.a = cpu.ram.read(address + cpu.y)
      cycles -= 1

  cpu = updateFlags(cpu, cpu.a)

  return cpu, cycles