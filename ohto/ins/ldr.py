ldx_codes = [0xA2, 0xAE, 0xBE, 0xA6, 0xB6]
ldy_codes = [0xA0, 0xAC, 0xBC, 0xA4, 0xB4]
codes = ldx_codes + ldy_codes

def updateFlags(cpu, value: int) -> None:
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  register = cpu.x if opcode in ldx_codes else cpu.y
  index = 'x' if opcode in ldx_codes else 'y'
  if opcode == 0xA2 or opcode == 0xA0: # LDX or LDY immediate
    register = cpu.ram.read(cpu.pc)
    cpu.pc += 1
    cycles -= 1
  elif opcode == 0xA6 or opcode == 0xA4: # LDX or LDY zero page
    zero_page_address = cpu.ram.read(cpu.pc)
    cycles -= 1
    register = cpu.ram.read(zero_page_address)
    cpu.pc += 1
    cycles -= 1
  elif opcode == 0xAE or opcode == 0xAC: # LDX or LDY absolute
    address = cpu.ram.read16(cpu.pc)
    cpu.pc += 2
    cycles -= 2
    register = cpu.ram.read(address)
    cycles -= 1
  elif opcode == 0xBE or opcode == 0xBC: # LDX or LDY absolute, X
    address = cpu.ram.read16(cpu.pc)
    cpu.pc += 2
    cycles -= 2
    if index == 'x':
      register = cpu.ram.read(address + cpu.x)
    else:
      register = cpu.ram.read(address + cpu.y)
    cycles -= 1

  if opcode in ldx_codes:
    cpu.x = register
  else:
    cpu.y = register

  cpu = updateFlags(cpu, register)
  return cpu, cycles