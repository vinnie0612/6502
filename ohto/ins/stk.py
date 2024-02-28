pha_codes = [0x48]
php_codes = [0x08]
pla_codes = [0x68]
plp_codes = [0x28]
codes = pha_codes + php_codes + pla_codes + plp_codes

def updateFlags(cpu, value: int):
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  if opcode in pha_codes:
    cpu.ram.write(0x0100 + cpu.sp, cpu.a)
    cycles -= 1
    cpu.sp -= 1

  elif opcode in php_codes:
    cpu.ram.write(0x0100 + cpu.sp, int(''.join([str(int(cpu.flags[flag])) for flag in cpu.flags]), 2))
    cycles -= 1
    cpu.sp -= 1

  elif opcode in pla_codes:
    cpu.a = cpu.ram.read(0x0100 + cpu.sp)
    cycles -= 2
    cpu.sp += 1
    cpu = updateFlags(cpu, cpu.a)

  elif opcode in plp_codes:
    cpu.sp += 1
    cpu.flags = {
      'c': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00000001),
      'z': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00000010),
      'i': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00000100),
      'd': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00001000),
      'b': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00010000),
      'v': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b00100000),
      'n': bool(cpu.ram.read(0x0100 + cpu.sp) & 0b01000000)
    }
    cycles -= 2

  cycles -= 1
  return cpu, cycles
