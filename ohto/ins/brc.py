codes = [0x90, 0xB0, 0xF0, 0x30, 0xD0, 0x10, 0x50, 0x70]

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x90: # BCC
      if not cpu.flags['c']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0xB0: # BCS
      if cpu.flags['c']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0xF0: # BEQ
      if cpu.flags['z']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0x30: # BMI
      if cpu.flags['n']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0xD0: # BNE
      if not cpu.flags['z']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0x10: # BPL
      if not cpu.flags['n']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0x50: # BVC
      if not cpu.flags['v']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

    case 0x70: # BVS
      if cpu.flags['v']:
        offset = cpu.ram.read(cpu.pc)
        cpu.pc += 1
        cycles -= 1
        if offset & 0x80:
          offset -= 0x100
        cpu.pc += offset
        cycles -= 1

  return cpu, cycles