codes = [0x18, 0xD8, 0x58, 0xB8, 0x38, 0xF8, 0x78]

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x18: # CLC
      cpu.flags['c'] = False
      cycles -= 1

    case 0xD8: # CLD
      cpu.flags['d'] = False
      cycles -= 1

    case 0x58: # CLI
      cpu.flags['i'] = False
      cycles -= 1

    case 0xB8: # CLV
      cpu.flags['v'] = False
      cycles -= 1

    case 0x38: # SEC
      cpu.flags['c'] = True
      cycles -= 1

    case 0xF8: # SED
      cpu.flags['d'] = True
      cycles -= 1

    case 0x78: # SEI
      cpu.flags['i'] = True
      cycles -= 1