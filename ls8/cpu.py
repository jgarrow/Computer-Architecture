"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory
        self.reg = [0] * 8 # 8 registers
        self.pc = 0 
        self.running = False
        self.commands = {
            0b00000001: self.hlt, # HLT: halt the CPU and exit the emulator
            0b10000010: self.ldi, # LDI: load "immediate", store a value in a register, or "set this register to this value"
            0b01000111: self.prn, # PRN: a pseudo-instruction that prints the numeric value stored in a register
            0b10100010: self.mul, # MUL: multiplyt the values in 2 registers together
            0b01000101: self.push, # PUSH the value in the given register on the stack
            0b01000110: self.pop # POP the value at the top of the stack into the given register
        }

    # Inside the CPU, there are two internal registers used for memory operations: the Memory Address Register (MAR) and the Memory Data Register (MDR). 
    # The MAR contains the address that is being read or written to. The MDR contains the data that was read or the data to write. 
    # You don't need to add the MAR or MDR to your CPU class, but they would make handy parameter names for `ram_read()` and `ram_write()`
    
    # mar = Memory Address Register
    def ram_read(self, mar):
        return self.ram[mar]
    
    # mar = Memory Address Register
    # mdr = Memory Data Register
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    
    # halt the CPU and exit the emulator
    def hlt(self):
        self.running = False
        sys.exit()
        
        
    # LDI register immediate
    # Set the value of a register to an integer
    def ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = operand_b
        self.pc += 3
        self.running = True
        
    
    # PRN register pseudo-instruction
    # print the numeric value stored in a register
    def prn(self):
        operand_a = self.ram_read(self.pc + 1)

        print(self.reg[operand_a])
        self.pc += 2
        self.running = True
    
    def mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3
        self.running = True
    
    def push(self):
        # decrement the SP (stack pointer)
        self.reg[7] -= 1

        # copy value from given register into address pointed to by SP
        register_address = self.ram_read(self.pc + 1)
        value = self.reg[register_address]

        sp = self.reg[7]
        self.ram_write(sp, value)
        self.pc += 2

    def pop(self):
        # copy the value from the address pointed to by `SP` to the given register

        # get the SP
        sp = self.reg[7]

        # copy the value from memory at that SP address
        value = self.ram_read(sp)

        # get the target register address
        register_address = self.ram_read(self.pc + 1)

        # Put the value in that register
        self.reg[register_address] = value

        # Increment the SP (move it back up)
        self.reg[7] += 1
        self.pc += 2



    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     print(f'instruction: {instruction}')
        #     self.ram[address] = instruction
        #     address += 1
        
        # print(self.ram)

        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}: missing filename argument')
                print(f'Usage: python3 {sys.argv[0]} <somefilename>')
                sys.exit(1)

            # add a counter that adds to memory at that index
            ram_index = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#")[0]
                    stripped_split_line = split_line.strip()

                    if stripped_split_line != "":
                        command = int(stripped_split_line, 2)
                        
                        # load command into memory
                        self.ram_write(ram_index, command)
                        ram_index += 1

        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram_read(self.pc) # instruction register/command

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.commands[ir]()



    
