brk_code = 0x00
jmp_codes = [0x4C, 0x6C]
jsr_code = 0x20
rti_code = 0x40
rts_code = 0x60
codes = jmp_codes + [jsr_code, rti_code, rts_code, brk_code]

def runInstruction(opcode, cpu, cycles):
  match opcode:
    case 0x4C: # JMP absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc = address
      cycles -= 2

    case 0x6C: # JMP indirect
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      indirect_address = cpu.ram.read16(address)
      cpu.pc = indirect_address
      cycles -= 4

    case 0x20: # JSR absolute
      address = cpu.ram.read16(cpu.pc)
      cpu.pc += 2
      cpu.push16(cpu.pc - 1)
      cpu.pc = address
      cycles -= 5

    case 0x40: # RTI
      cpu.flags = cpu.pop8()
      cpu.pc = cpu.pop16()
      cycles -= 5

    case 0x60: # RTS
      cpu.pc = cpu.pop16() + 1
      cycles -= 5

    case 0x00: # BRK
      cpu.pc += 1
      cpu.ram.write(0x0100 + cpu.sp, (cpu.pc >> 8) & 0xFF)
      cpu.sp = (cpu.sp - 1) & 0xFF
      cpu.ram.write(0x0100 + cpu.sp, cpu.pc & 0xFF)
      cpu.sp = (cpu.sp - 1) & 0xFF
      cpu.flags['u'] = 1

      flags = ["1" if cpu.flags[x] else "0" for x in ['c', 'z', 'i', 'd', 'b', 'u', 'v', 'n']]

      cpu.ram.write(0x0100 + cpu.sp, int("".join(flags), 2))

      cpu.sp = (cpu.sp - 1) & 0xFF
      cpu.flags['i'] = 1
      cpu.pc = cpu.ram.read16(0xFFFE)
      cycles -= 6

  return cpu, cycles