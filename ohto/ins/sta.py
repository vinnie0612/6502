codes = [0x8D, 0x9D, 0x99, 0x85, 0x95, 0x81, 0x91]

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x8D:  # STA absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.ram.write(address, cpu.a)
      cycles -= 1

    case 0x9D:  # STA absolute, X
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.ram.write(address + cpu.x, cpu.a)
      cycles -= 2

    case 0x99:  # STA absolute, Y
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cycles -= 2
      cpu.ram.write(address + cpu.y, cpu.a)
      cycles -= 2

    case 0x85:  # STA zero page
      zero_page_address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      cycles -= 1
      cpu.ram.write(zero_page_address, cpu.a)
      cycles -= 1

    case 0x95:  # STA zero page, X
      zero_page_address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      cycles -= 1
      cpu.ram.write(zero_page_address + cpu.x, cpu.a)
      cycles -= 2

    case 0x81:  # STA zero page, X (indirect)
      zero_page_address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      cycles -= 1
      effective_address = cpu.ram.read16(zero_page_address + cpu.x)
      cpu.ram.write(effective_address, cpu.a)
      cycles -= 4

    case 0x91:  # STA zero page, Y (indirect)
      zero_page_address = cpu.ram.read(cpu.pc)
      cpu.pc += 1
      cycles -= 4
      effective_address = cpu.ram.read16(zero_page_address + cpu.y)
      cpu.ram.write(effective_address, cpu.a)
      cycles -= 4

  return cpu, cycles

