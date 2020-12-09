"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # 8 general-purpose registers (8-bit)
        self.ram = [0] * 256  # 256 bytes of memory
        self.pc = 0  # program counter
        self.reg[7] = 0xF4  # SP (Stack Pointer)

        # Instruction definition
        # LDI - This instruction sets a specified register to a specified value
        self.SAVE = 0b10000010  # LDI
        self.PRINT_REG = 0b01000111
        # HLT to be similar to Python's `exit()`
        self.HALT = 0b00000001  # HLT
        self.MULT = 0b10100010
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.ADD = 0b10100000

    def ram_read(self, address):
        '''
        accept the address to read and return the value stored there.
        '''
        # Return the binary representation of an integer.
        # return bin(self.ram[address])
        return self.ram[address]

    def ram_write(self, value, address):
        '''
        accept a value to write, and the address to write it to.
        '''
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def load_ram(self):
        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}: missing filename argument')
                print(f'Usage: python3 {sys.argv[0]} <filename>')
                sys.exit(1)

            # add a counter that adds to memory at that index
            ram_index = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#")[0]
                    strtipped_split_line = split_line.strip()

                    if strtipped_split_line != "":
                        command = int(strtipped_split_line, 2)

                        # load command into memory
                        self.ram[ram_index] = command

                        ram_index += 1

        except FileNotFoundError:
            print(f'Error from {sys.srgv[0]}: {sys.argv[1]} not found')
            print('Please double check the file name')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True
        # self.pc = 0

        while running:
            command = self.ram[self.pc]

            # SAVE
            if command == self.SAVE:
                num_to_save = self.ram[self.pc + 1]
                register_address = self.ram[self.pc + 2]
                self.reg[num_to_save] = register_address
                # self.pc += 2  # (command >> 6)

            # PRINT_REG
            elif command == self.PRINT_REG:
                reg_address = self.ram[self.pc + 1]
                print(self.reg[reg_address])
                # same
                # print(self.reg[self.ram_read(self.pc + 1)])
                # self.pc += (command >> 6)

            elif command == self.ADD:
                reg1_address = self.ran[self.pc + 1]
                reg2_address = self.ram[self.pc + 2]

                self.reg[reg1_address] += self.reg[reg2_address]

            # MULT
            elif command == self.MULT:
                reg1_address = self.ram[self.pc + 1]
                reg2_address = self.ram[self.pc + 2]

                # self.reg[reg1_address] = self.reg[reg1_address] * self.reg[reg2_address]
                self.reg[reg1_address] *= self.reg[reg2_address]

            elif command == self.PUSH:
                self.reg[7] -= 1

                register_address = self.ram[self.pc + 1]
                value = self.reg[register_address]

                SP = self.reg[7]
                self.ram[SP] = value

            elif command == self.POP:
                SP = self.reg[7]

                value = self.ram[SP]

                register_address = self.ram[self.pc + 1]

                self.reg[register_address] = value

                self.reg[7] += 1

            # HLT
            elif command == self.HALT:
                running = False

            number_of_operands = command >> 6
            self.pc += (1 + number_of_operands)

            # self.pc += 1
