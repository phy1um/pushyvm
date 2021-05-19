---
title: Stack VM
...
## Basics

Programs are executed in a **machine**. A machine consists of **memory** and **registers**. Memory contains a **program**, which is a list of **codes**, plus a **stack**. All codes and stack values are 2 bytes.

### Codes
A code is a 2-byte machine instruction. It can be separated into 2 parts, the first byte is the *Op* and the second byte is the *Arg*. Op determines what kind of action will be performed, while Arg allows this operation to be customized, sometimes beyond the ISA specification such as in the case of interrupts.

### Registers
The VM contains 4 registers named A, B, SP and PC. They behave as follows:

#### SP Register
The Stack Pointer (SP) is a reference in memory to the current head of the stack. Pushing will write a value to MEMORY[SP], then decrement SP. Popping from the stack will increment SP, then return MEMORY[SP]

#### PC Register
The Program Counter (PC) is a reference to the location in memory of the next code to execute. When the machine updates, it evaluates the code at MEMORY[SP] and advances PC by at least one - with the exception of jump and branch instructions which can also move PC backwards.

#### A and B register
The are temporary registers used for computations. Elements are popped off of the stack into a register. They are internal to the implementation of the ISA and should not be important outside of implementing core operations.


## Arithmetic

|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Add|0x2|?|[a b]|[c]| c = a+b|
|Sub|0x4|?|[a b]|[c]| c = a-b|
|Mul|0x6|?|[a b]|[c]| c = a\*b|
|Div|0x8|?|[a b]|[c]| c = a / b|
|Mod|0xa|?|[a b]|[c]| c = a % b|

## Stack Manipulation
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Lli|0x50|a|[]|[a]|Load 1byte value to stack|
|Lbi|0x52|?|[]|[a]|a = \*(PC+1); PC += 2|
|Pop|0x54|0x0|[a]|[]|Remove top of stack|
|Pop[x]|0x54|0x1-0xf|[a]|[]|Remove top of stack, writing to machine port|
|Dup|0x56|?|[a]|[a a]|Duplicate top of stack|

## Control
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Jmp|0x60|0|[a b]|[]|PC=b|
|Jmp|0x60|1|[a b]|[]|PC+=b|
|JIm|0x62|0|[]|[]|PC=\*(PC+1)|
|JIm|0x62|1|[]|[]|PC+=\*(PC+1)|
|Bx?|0x64|0|[a b]|[]|IF a != 0 THEN PC=b|
|Bx?|0x64|1|[a b]|[]|IF a != 0 THEN PC+=b|
|Bi?|0x66|0|[a]|[]|IF a != 0 THEN PC=\*(PC+1)|
|Bi?|0x66|1|[a]|[]|IF a != 0 THEN PC+=\*(PC+1)|

## Logic
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|GT|0x20|0|[a b]|[c]|c = IF a > b THEN 1 ELSE 0|
|GTE|0x20|1|[a b]|[c]|c = IF a >= b THEN 1 ELSE 0|
|LT|0x22|0|[a b]|[c]|c = IF a < b THEN 1 ELSE 0|
|LTE|0x22|1|[a b]|[c]|c = IF a <= b THEN 1 ELSE 0|
|EQ|0x24|0|[a b]|[c]|c = IF a = b THEN 1 ELSE 0|
|NEQ|0x24|1|[a b]|[c]|c = IF a != b THEN 1 ELSE 0|
|NOT|0x26|0|[a]|[b]|b = IF a != 0 THEN 0 ELSE 1|
|AND|0x28|0|[a b]|[c]|c = a & b|
|OR|0x2a|0|[a b]|[c]|c = a \| b|
|XOR|0x2c|0|[a b]|[c]|c = a XOR b|
|SHL|0x2e|x|[a]|[c]|c = a << x|
|SHR|0x30|x|[a]|[c]|c = a >> x|

## Machine
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|SYS[INITMEM]|0x70|0|[a]|[]|Initialize machine with 2\*a bytes of memory|
|SYS[COPY]|0x70|1|[a b]|[]|Copy the next a codes to address starting at b; PC += a|
|SYS[STACKADDR]|0x70|2|[a]|[]|Set stack address to PC+1; PC += 2|
|INT[x]|0x71|x|?|?|Flag system interrupt, stack can be modified as handler sees fit|

