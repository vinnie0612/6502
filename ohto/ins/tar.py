tax_codes = [0xAA]
tay_codes = [0xA8]
tsx_codes = [0xBA]
txa_codes = [0x8A]
txs_codes = [0x9A]
tya_codes = [0x98]
codes = tax_codes + tay_codes + tsx_codes + txa_codes + txs_codes + tya_codes

def updateFlags(cpu, value: int) -> None:
  cpu.flags['z'] = (value & 0b11111111) == 0
  cpu.flags['n'] = (value & 0b10000000) > 0
  return cpu

def runInstruction(opcode, cpu, cycles):
  if opcode in tax_codes:
    cpu.x = cpu.a
  elif opcode in tay_codes:
    cpu.y = cpu.a
  elif opcode in tsx_codes:
    cpu.x = cpu.sp
  elif opcode in txa_codes:
    cpu.a = cpu.x
  elif opcode in txs_codes:
    cpu.sp = cpu.x
  elif opcode in tya_codes:
    cpu.a = cpu.y

  if opcode not in txs_codes:
    cpu = updateFlags(cpu, cpu.a)
  cycles -= 1
  return cpu, cycles