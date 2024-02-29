import os
import time
import importlib.util

class CPU:
  def __init__(self, ram, singleStep=True, delay=0.1, debug=True) -> None:
    print(f"OHTO CPU Emulator - by Tamás Vince")
    ins_path = os.path.join(os.path.dirname(__file__), 'ins')
    self.instructions = []
    for file in os.listdir(ins_path):
      if file.endswith('.py'):
        spec = importlib.util.spec_from_file_location(file[:-3], os.path.join(ins_path, file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.instructions.append(module)
    print(f"Loaded {sum([len(ins.codes) for ins in self.instructions])} instructions")
    self.singleStep = singleStep
    self.delay = delay
    self.debug = debug

    self.ram = ram
    self.pc = 0xFFFC
    self.sp = 0x0100

    self.a = 0
    self.x = 0
    self.y = 0

    self.flags = {
      'c': False,
      'z': False,
      'i': False,
      'd': False,
      'b': False,
      'u': False,
      'v': False,
      'n': False
    }
    if self.debug: self.print_status(0, 0)
    input("Initialized, press enter to continue...")

  def push8(self, value: int) -> None:
    self.ram.write(0x0100 + self.sp, value)
    self.sp -= 1
    self.verifyStackPointerBounds()

  def push16(self, value: int) -> None:
    self.push8((value >> 8) & 0xFF)
    self.push8(value & 0xFF)

  def pop8(self) -> int:
    self.sp += 1
    self.verifyStackPointerBounds()
    return self.ram.read(0x0100 + self.sp)

  def pop16(self) -> int:
    low = self.pop8()
    high = self.pop8()
    return (high << 8) | low


  def print_status(self, opcode, cycles):
    print(f"""
    OUTPUT: {self.ram.output}
    CYCLES: {cycles if cycles > 0 else f"Forever mode - {abs(cycles)}"}
    OPCODE: {opcode:02X}
    PC: {self.pc:04X}
    SP: {self.sp:04X}
    A: {self.a:02X} X: {self.x:02X} Y: {self.y:02X}
    FLAGS: \n{'\n'.join([f"\t{k}: {int(v)}" for k, v in self.flags.items()])}
    """)

  def reset(self):
    self.pc = self.ram.read16(0xFFFC)

    self.sp = 0x01FF
    self.a, self.x, self.y = 0, 0, 0
    self.flags = {
      'c': False,
      'z': False,
      'i': False,
      'd': False,
      'b': False,
      'v': False,
      'n': False
    }
    print(f"Reset CPU to PC: 0x{self.pc:04X}")

  def verifyStackPointerBounds(self):
    if self.sp < 0x0100 or self.sp > 0x01FF:
      print(f"Stack pointer out of bounds: {self.sp:04X}")
      return False
    return True

  def execute(self, cycles=0, forever=False) -> None:
    if forever: input("Running in forever mode - use JAM (0x02) to stop execution. (enter to continue...)")
    while cycles > 0 or forever:
      opcode = self.ram.read(self.pc)
      opcodeMatched = False
      self.pc += 1
      cycles -= 1

      for ins in self.instructions:
        if opcode in ins.codes:
          if self.debug: print(f"Running instruction: {ins.__name__} with opcode {opcode:02X} from 0x{self.pc:04X}")
          self, cycles = ins.runInstruction(opcode, self, cycles)
          opcodeMatched = True
          break
      if not opcodeMatched:
        match opcode:
          case 0xEA:  # NOP
            cycles -= 1

          case _:
            print(f"Last opcode: {self.ram.read(self.pc-1):02X}")
            self.print_status(opcode, cycles)
            print(f'Opcode not implemented: {opcode:02X}')
            exit()

      if self.debug: self.print_status(opcode, cycles)
      if not self.verifyStackPointerBounds():
        break
      if self.singleStep:
        input("Single stepping")
      else:
        time.sleep(self.delay)