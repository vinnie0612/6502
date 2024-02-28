stx_codes = [0x8E, 0x86, 0x96]
sty_codes = [0x8C, 0x84, 0x94]
codes = stx_codes + sty_codes

def runInstruction(opcode, cpu, cycles):
  register = cpu.x if opcode in stx_codes else cpu.y
  index = 'x' if opcode in stx_codes else 'y'
  if opcode == 0x8E or opcode == 0x8C: # STX or STY absolute
    address = cpu.ram.read16(cpu.pc)
    cpu.pc += 2
    cycles -= 2
    cpu.ram.write(address, register)
    cycles -= 1

  elif opcode == 0x86 or opcode == 0x84: # STX or STY zero page
    zero_page_address = cpu.ram.read(cpu.pc)
    cpu.pc += 1
    cycles -= 1
    cpu.ram.write(zero_page_address, register)
    cycles -= 1

  elif opcode == 0x96 or opcode == 0x94: # STX or STY zero page, R-indexed
    zero_page_address = cpu.ram.read(cpu.pc)
    cpu.pc += 2
    cycles -= 1

    if index == 'x':
      cpu.ram.write(zero_page_address + cpu.x, register)
    else:
      cpu.ram.write(zero_page_address + cpu.y, register)
    cycles -= 2

  if opcode in stx_codes:
    cpu.x = register
  else:
    cpu.y = register

  return cpu, cycles