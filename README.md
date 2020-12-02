# Computer Architecture

Until now, the computer itself has been something of a mysterious black box that miraculously executes our instructions for us. This sprint will explore how computers work at a very low level, giving you additional perspective that helps you approach the software development with more confidence.

## Computer Architecture: Basics, Number Bases

The basics of how a computer is constructed and functions. Practice manipulating numbers in binary and hexadecimal.

Project is an implementation of an emulator for the LS-8 computer.

**Objectives:**

- Describe the functional components of a CPU
- Convert between and understand decimal, binary, and hexadecimal

## Computer Architecture: Bitwise Operations

Computers operate with 1s and 0s, and there are several operations we can perform on numbers that are similar to the boolean operations you’ve already used: and, or, not, and so on.

Practice some of those bitwise operations to see how the computer makes use of them to get work done.

**Objectives:**

- Perform basic bitwise operations

## Computer Architecture: The System Stack

How peripherals connect to and interact with the rest of the system, and how requests to and from the peripherals are processed in a timely manner.

**Objectives:**

- Describe the CPU stack and how it's useful
- Dscribe how interrupts work and why they're useful

## Computer Architecture: Subroutines, CALL/RET

Down at the machine level, functions are known as subroutines. You can call them and return from them, just like functions in higher-level languages.

How the CPU makes use of the system stack to make this happen.

How higher-level languages improve on this to allow for argument passing and return values.

**Objectives:**

- Describe how the CPU handles subroutines

## Project

*[Implement the LS-8 Emulator](ls8/)

## Task List: add this to the first comment of your Pull Request

### Day 1: Get `print8.ls8` running

- [ ] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction

### Day 2: Add the ability to load files dynamically, get `mult.ls8` running

- [ ] Un-hardcode the machine code
- [ ] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [ ] Implement a Multiply instruction (run `mult.ls8`)

### Day 3: Stack

- [ ] Implement the System Stack and be able to run the `stack.ls8` program

### Day 4: Get `call.ls8` running

- [ ] Implement the CALL and RET instructions
- [ ] Implement Subroutine Calls and be able to run the `call.ls8` program

### Stretch

- [ ] Add the timer interrupt to the LS-8 emulator
- [ ] Add the keyboard interrupt to the LS-8 emulator
- [ ] Write an LS-8 assembly program to draw a curved histogram on the screen
