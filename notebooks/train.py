'''
>>> 0b10101
21
>>> 0xE3
227
>>> hex(27)
'0x1b'
>>> hex(227)
'0xe3'
>>> bin(12)
'0b1100'
>>> int('123')
123
>>> int('10101', 2)
21
>>> int('e3', 16)
227
>>> num = 123
>>> f'{num:x}'
'7b'
>>> f'{num:b}'
'1111011'
'''

PRINT_TIM = 0b00000001
HALT =      0b00000010
PRINT_NUM = 0b00000011  # a 2-byte command, takes 1 arguments
SAVE =      0b00000100  # a 3-byte command, takes 2 arguments
PRINT_REG = 0b00000101
PRINT_SUM = 0b00000110

# a data-driven machine
# function call
# a 'variable' == registers for our programs to save things into

# RAM
memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,  # print 99 or some other number
    42,
    SAVE,  # save 99 into register 2  <-- PC
    99,  # the number to save
    2,  # the register to put it into
    PRINT_REG,
    2,
    PRINT_SUM,  # R1 + R2
    HALT,
]

# registers, R0-R7
registers = [0] * 8

running = True

# program counter
pc = 0

while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print('tim!')

    elif command == PRINT_NUM:
        num_to_print = memory[pc + 1]  # we already incremented PC!
        print(num_to_print)

        pc += 1  # but increment again

    elif command == SAVE:
        num_to_save = memory[pc + 1]
        register_address = memory[pc + 2]

        registers[register_address] = num_to_save

        # shorter:
        # registers[memory + 2] = memory[pc + 1]

        pc += 2

    elif command == PRINT_REG:
        reg_address = memory[pc + 1]

        saved_number = registers[reg_address]

        print(saved_number)

    elif command == HALT:
        running = False

    pc += 1  # so we don't get sucked into an infinite loop!
