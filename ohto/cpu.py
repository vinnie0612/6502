import os
import importlib.util

ins_path = os.path.join(os.path.dirname(__file__), 'ins')
instructions = []
for file in os.listdir(ins_path):
  if file.endswith('.py'):
    spec = importlib.util.spec_from_file_location(file[:-3], os.path.join(ins_path, file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    instructions.append(module)

class CPU:
  def __init__(self, ram) -> None:
    self.ram = ram
    self.pc = 0xFFFC
    self.sp = 0

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

  def print_status(self, opcode):
    print(f"""
    OPCODE: {opcode:02X}
    PC: {self.pc:04X}
    SP: {self.sp:04X}
    A: {self.a:02X} X: {self.x:02X} Y: {self.y:02X}
    FLAGS: \n{'\n'.join([f"\t{k}: {int(v)}" for k, v in self.flags.items()])}
    """)

  def reset(self):
    self.ram.initialize()

    self.pc = 0xFFFC
    self.sp = 0x0100
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

  def execute(self, cycles: int) -> None:
    while cycles > 0:
      opcode = self.ram.read(self.pc)
      opcodeMatched = False
      self.pc += 1
      cycles -= 1

      for ins in instructions:
        if opcode in ins.codes:
          self, cycles = ins.runInstruction(opcode, self, cycles)
          opcodeMatched = True
          break
      if not opcodeMatched:
        match opcode:
          case 0xEA:  # NOP
            cycles -= 1

          case 0x20:  # JSR absolute
            subAddr = self.ram.read16(self.pc)
            self.pc += 2
            cycles -= 2

            self.ram.write16(0x0100 + self.sp, self.pc - 1)
            cycles -= 2
            self.sp -= 2
            self.pc = subAddr
            cycles -= 1

          case _:
            print(f'Opcode not implemented: {opcode:02X}')
            cycles = 0
      self.print_status(opcode)
      input("Single stepping")