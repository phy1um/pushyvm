import struct
import sys

opwords = {}

def parse_arg(s):
    parts = s.split("[")
    if len(parts) == 1:
        return s,""
    else:
        return parts[0], parts[1][:-1]

MAX_2B = 2**16 - 1
def encode_2byte(t):
    enc_tape = []
    for b in t:
        if not isinstance(b, int):
            raise Exception("All values on tape must be integers")
        if b > MAX_2B:
            raise Exception("All values on tape must be 2bytes max")
        if b < 0:
            raise Exception("Negative numbers not currently supported")
        enc_tape.append(b)
    return enc_tape
         
def encode_2byteM(t):
    n = len(t)
    fmt = f">{n}h"
    return struct.pack(fmt, *t)
     

def compile(s):
    tape = []
    for line in s.split("\n"):
        print("Compiling " + line)
        if len(line) < 1:
            continue
        if line[0] == ";":
            continue
        toks = line.split(" ")
        op_arg = toks[0]
        rest = ""
        if len(toks) > 1:
            rest = " ".join(toks[1:])
        op,arg = parse_arg(op_arg) 
        if op not in opwords:
            raise Exception(f"Unknown op {op}")
        print(f" -> {op}[{arg}] :: {rest}")
        f = opwords[op]
        b = f(arg, rest)
        print(" --", end="")
        for by in b:
            print(f" {by:#x}", end="")
        print()
        tape += b
    return encode_2byteM(tape)
    
def define_word(op, f):
    opwords[op] = f

def op_lit(v):
    def f(a,r):
        arg_val = 0
        if a != "":
            arg_val = int(a)
        print(f"EMIT LIT: {v:#x}:{arg_val:#x}")
        return [(v<<8) + arg_val]
    return f

def op_load_imm_next(v):
    def f(a, rest):
        imm = int(rest)
        op_word = op_lit(v)(a,"")
        return [op_word[0],imm]
    return f

def inline_byte(a, rest):
    v = int(rest)
    return [v]

# Arithmetic
define_word("add", op_lit(0x2))
define_word("sub", op_lit(0x4))
define_word("mul", op_lit(0x6))
define_word("div", op_lit(0x8))
define_word("mod", op_lit(0xa))

# Stack
define_word("lii", op_lit(0x50))
define_word("lbi", op_lit(0x52))
define_word("pop", op_lit(0x54))
define_word("dup", op_lit(0x56))

# Control
define_word("jmp", op_lit(0x60))
define_word("jim", op_lit(0x62))
define_word("bx?", op_lit(0x64))
define_word("bi?", op_lit(0x66))

# Logic
define_word("gt", op_lit(0x20))
define_word("lt", op_lit(0x22))
define_word("eq", op_lit(0x24))
define_word("not", op_lit(0x26))

define_word("SYS", op_lit(0x70))
define_word("INT", op_lit(0x71))

define_word(":", inline_byte)


if __name__ == "__main__":
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    with open(file_in, "r") as f:
        body = f.read()
        prog = compile(body)
        with open(file_out, "wb") as o:
            o.write(prog)

