---
title: Stack VM
...
## Basics

Programs are executed in a **machine**. A machine consists of **memory** and **registers**. Memory contains a **program**, which is a list of **codes**, plus a **stack**. All codes and stack values are 2 bytes.

### Codes
A code is a 2-byte machine instruction. It can be separated into 2 parts, the first byte is the *Op* and the second byte is the *Arg*. Op determines what kind of action will be performed, while Arg allows this operation to be customized, sometimes beyond the ISA specification such as in the case of interrupts.

### Registers
The VM contains 3 registers named TGT, SP and PC. They behave as follows:

#### SP Register
The Stack Pointer (SP) is a reference in memory to the current head of the stack. Pushing will write a value to RAM[SP], then decrement SP. Popping from the stack will increment SP, then return RAM[SP]

#### PC Register
The Program Counter (PC) is a reference to the location in memory of the next code to execute. When the machine updates, it evaluates the code at RAM[SP] and advances PC by at least one - with the exception of jump and branch instructions which can also move PC backwards.

#### TGT Register
The TGT register is used as an intermediate location between completed calculations/memory access and the stack.

## Arithmetic

|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Add|0x2|0|[a b]|[c]| c = a+b|
|Sub|0x4|0|[a b]|[c]| c = a-b|
|Mul|0x6|0|[a b]|[c]| c = a\*b|
|Div|0x8|0|[a b]|[c]| c = a / b|
|Mod|0xa|0|[a b]|[c]| c = a % b|

If Arg=1 then the TGT register is set to the result and nothing is pushed to the stack


## Stack Manipulation
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Ldi|0x50|a|[]|[a]|RAM[SP--] = a|
|Ldp|0x52|?|[]|[a]|RAM[SP--] = RAM[PC+1]; PC += 2; (Load 2 byte immediate from program to stack)|
|Pop|0x54|0|[a]|[]|TGT = a|
|Pop[x]|0x54|0x1-0xf|[a]|[]|Port[x] <- a|
|Dup|0x56|?|[a]|[a a]|v=RAM[SP]; RAM[SP--]v;|
|Rot|0x58|?|[a b c]|[b c a]|Rotate top 3 elements of stack|
|Swp|0x5a|?|[a b]|[b a]|Swap head elements|
|Del|0x5c|0|[a]|[]|SP++|
|Psh|0x5e|0|[]|[a]|RAM[SP++] = TGT|

|Ldm|0x40|0|[x]|[]| TGT = RAM[x]|
|Set|0x42|0|[x]|[]| RAM[x] = TGT|

## Control
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|Jmp|0x60|0|[a]|[]|PC=a|
|Jmr|0x60|1|[a]|[]|PC+=a|
|Bx?|0x64|0|[a b]|[]|IF b != 0 THEN PC=a|
|Bx?|0x64|1|[a b]|[]|IF b != 0 THEN PC+=a|

## Logic
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|GT|0x20|0|[a b]|[c]|c = IF a > b THEN 1 ELSE 0|
|GTE|0x22|1|[a b]|[c]|c = IF a >= b THEN 1 ELSE 0|
|LT|0x24|0|[a b]|[c]|c = IF a < b THEN 1 ELSE 0|
|LTE|0x26|1|[a b]|[c]|c = IF a <= b THEN 1 ELSE 0|
|EQ|0x28|0|[a b]|[c]|c = IF a = b THEN 1 ELSE 0|
|NEQ|0x2a|1|[a b]|[c]|c = IF a != b THEN 1 ELSE 0|
|NOT|0x2c|0|[a]|[b]|b = IF a != 0 THEN 0 ELSE 1|
|AND|0x2e|0|[a b]|[c]|c = a & b|
|OR|0x30|0|[a b]|[c]|c = a \| b|
|XOR|0x32|0|[a b]|[c]|c = a XOR b|
|SHL|0x34|x|[a]|[c]|c = a << x|
|SHR|0x36|x|[a]|[c]|c = a >> x|

## Machine
|Name|Op|Arg|Stack Before|Stack After|Description|
|---|---|---|---|---|---|
|SYS[INITMEM]|0x70|0|[a]|[]|Initialize machine with 2\*a bytes of memory|
|SYS[COPY]|0x70|1|[a b]|[]|Copy the next a codes to address starting at b; PC += a|
|SYS[STACKADDR]|0x70|2|[a]|[]|Set stack address to PC+1; PC += 2|
|INT[x]|0x71|x|?|?|Flag system interrupt x, stack can be modified as handler sees fit|

