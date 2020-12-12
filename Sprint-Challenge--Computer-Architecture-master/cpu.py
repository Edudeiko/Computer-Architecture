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
        self.FL = [0] * 8  # The register is made up of 8 bits.

        # Instruction definition
        # LDI - This instruction sets a specified register to a specified value
        self.SAVE = 0b10000010  # LDI
        self.PRINT_REG = 0b01000111  # PRN
        self.HALT = 0b00000001  # HLT to be similar to Python's `exit()`
        self.MULT = 0b10100010
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.ADD = 0b10100000
        self.CALL = 0b01010000
        self.JUMP = 0b01010100  # Jump to the address stored in the given register
        self.RET = 0b00010001
        self.CMP = 0b10100111  # Compare the values in two registers
        self.JEQ = 0b01010101  # If `equal` flag is set (true), jump to the address stored in the given register.
        self.JNE = 0b01010110  # If `E` flag is clear (false, 0), jump to the address stored in the given register.

    def ram_read(self, address):
        '''
        accept the address to read and return the value stored there.
        '''
        return self.ram[address]

    def ram_write(self, value, address):
        '''
        accept a value to write, and the address to write it to.
        '''
        self.ram[address] = value

    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010,  # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111,  # PRN R0
    #         0b00000000,
    #         0b00000001,  # HLT
    #     ]

    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    def load_ram(self):
        '''python3 ls8.py sctest.ls8'''
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
        elif op == 'CMP':
            '''
            The flags register `FL` holds the current flags status. These flags
            can change based on the operands given to the `CMP` opcode.
            * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
            zero otherwise.
            * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
            registerB, zero otherwise.
            * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
            otherwise.
            '''
            if self.reg[reg_a] < self.reg[reg_b]:

                self.FL[0] = 1
                self.FL[1] = 0
                self.FL[2] = 0

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL[1] = 1
                self.FL[0] = 0
                self.FL[2] = 0

            else:
                self.FL[2] = 1
                self.FL[0] = 0
                self.FL[1] = 0

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
                reg1_address = self.ram[self.pc + 1]
                reg2_address = self.ram[self.pc + 2]

                # self.alu('ADD', reg1_address, reg2_address)
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

            elif command == self.CALL:
                # 1. push return address into Stack
                # find the address/index of the command AFTER call
                next_command_address = self.pc + 2

                # push the address into Stack
                # decrement the SP
                self.reg[7] -= 1

                # put the next command address at the location in memory
                # where the stack pointer points
                SP = self.reg[7]
                self.ram[SP] = next_command_address

                # 2. jump, set the PC to wherever the register says
                # find the number of the register to look at
                register_address = self.ram[self.pc + 1]

                # get the address of the subroutine out of that register
                address_to_jump = self.reg[register_address]

                # set the pc
                self.pc = address_to_jump

            elif command == self.RET:
                # Pop the value from the top of the stack and store it in the `PC`

                # Pop from top of stack
                # get the value first
                SP = self.reg[7]
                return_address = self.ram[SP]

                # then move the stack pointer back up
                self.reg[7] += 1

                # jump back, set PC to this value
                self.pc = return_address

            elif command == self.CMP:
                reg1 = self.ram_read(self.pc + 1)
                # reg1 = self.ram[self.pc + 1]
                reg2 = self.ram_read(self.pc + 2)
                # reg2 = self.ram[self.pc + 2]
                self.alu('CMP', reg1, reg2)

            elif command == self.JEQ:
                if self.FL[2] == 1:
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2

            elif command == self.JUMP:
                reg = self.ram_read(self.pc + 1)
                self.pc = self.reg[reg]

            elif command == self.JNE:
                if self.FL[2] == 0:
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2

            # HLT
            elif command == self.HALT:
                running = False

            else:
                print('command is not recognized')
                sys.exit(1)

            number_of_operands = command >> 6

            # bit shift and mask to isolate the 'C' bit
            sets_pc_directly = ((command >> 4) & 0b001) == 0b001

            if not sets_pc_directly:
                self.pc += (1 + number_of_operands)

            # self.pc += 1
