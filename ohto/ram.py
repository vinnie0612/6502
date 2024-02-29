class RAM:
  def __init__(self, size: int) -> None:
    self.size = size
    self.memory = [0] * size
    self.output = ""

  def initialize_from_binary(self, filename: str) -> None:
    with open(filename, "rb") as f:
      data = f.read()
    print(f"Read {len(data)} bytes from {filename}")
    if self.size < len(data):
      print(f"WARNING: Binary file {filename} is larger than RAM size {self.size}")
      exit()
    elif self.size > len(data):
      print(f"WARNING: Binary file {filename} is smaller than RAM size {self.size}")
      exit()
    for i in range(len(data)):
      if data[i] != 0:
        self.memory[i] = data[i]

  def read(self, address: int) -> int:
    return self.memory[address]

  def read16(self, address: int) -> int:
    return self.memory[address] | (self.memory[address + 1] << 8)

  def write(self, address: int, value: int) -> None:
    if address == 0x6000:
      self.output += chr(value)
    else:
      self.memory[address] = value

  def write16(self, address: int, value: int) -> None:
    self.memory[address] = value & 0xFF
    self.memory[address + 1] = (value >> 8) & 0xFF

  def dump(self, start: int, end: int) -> None:
    for i in range(start, end, 8):
      print(f"{i:04X} ", end="")
      for j in range(8):
        print(f"{self.memory[i + j]:02X} ", end="")
      print()