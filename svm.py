import struct
import sys

def unpack_2b(b):
    n = len(b) // 2
    fmt = f">{n}h"
    return struct.unpack(fmt, b)

def get_op(d):
    return (d&0xff00) >> 8

def get_arg(d):
    return d&0xff

opfuncs = {}

class PortSink(object):
    def __init__(self):
        pass
    def write(self, b):
        pass

class Machine(object):
    def __init__(self, r):
        self.sp = 0
        self.pc = 0
        self.a = 0
        self.b = 0
        self.handlers = []
        self.init_memory(r)
        self.port = [PortSink()]*10
        self.halt = False

    def bind_port(self, i, f):
        self.port[i] = f

    def init_memory(self, m):
        self.ram = [0]*m
        self.sp = m-1

    def copy(self, words, to):
        for i,w in enumerate(words):
            self.ram[to+i] = w 

    def eval(self):
        cmd = self.readword()
        op = get_op(cmd)
        arg = get_arg(cmd)
        #print(f"Eval {op:#x}[{arg:#x}]")
        eval_fn = opfuncs[op]
        eval_fn(self, arg)

    def popa(self):
        v = self.pop()
        self.a = v

    def popb(self):
        v = self.pop()
        self.b = v

    def pop(self):
        self.sp += 1
        v = self.ram[self.sp]
        return v

    def push(self, v):
        self.ram[self.sp] = v
        self.sp -= 1

    def readword(self):
        v = self.ram[self.pc]
        self.pc += 1
        return v

    def __str__(self):
        head = f"VM ({len(self.ram)} bytes) - A={self.a} B={self.b} PC={self.pc} SP={self.sp}"
        stack = str(self.ram[self.sp+1:])
        return "\n".join([head, stack])
        
def arith_fn(f):
    def op(vm, arg):
        vm.popa()
        vm.popb()
        vm.push(f(vm.a, vm.b))
    return op

def lbi_op(vm, arg):
    imm = vm.readword()
    vm.push(imm)

def lii_op(vm, arg):
    vm.push(arg)

def pop_op(vm, arg):
    v = vm.pop()
    vm.port[arg].write(str(v)+"\n")

def jmp_op(vm, arg):
    vm.popa()
    vm.pc = vm.a

def jim_op(vm, arg):
    tgt = vm.readword()
    if arg == 0:
        vm.pc = tgt
    else:
        vm.pc += tgt-1

def dup_op(vm, arg):
    vm.popa()
    vm.push(vm.a)
    vm.push(vm.a)

def swp_op(vm, arg):
    vm.popa()
    vm.popb()
    vm.push(vm.a)
    vm.push(vm.b)

def shf_op(vm, arg):
    vm.popa()
    vm.popb()
    c = vm.pop()
    vm.push(vm.b)
    vm.push(c)
    vm.push(vm.a)

def cmp_fn(f):
    def op(vm, arg):
        vm.popa()
        vm.popb()
        if f(vm.a, vm.b):
            vm.push(1)
        else:
            vm.push(0)
    return op

def branch(vm, arg):
    vm.popa()
    vm.popb()
    if vm.b != 0:
        vm.pc = vm.a

def trigger_int(vm, arg):
    if arg == 0:
        vm.halt = True
    elif arg == 1:
        s = input("> ")
        v = int(s)
        vm.push(v)
    else:
        print("INVALID INTERRUPT: " + str(arg))
        vm.halt = True

opfuncs[0x2] = arith_fn(lambda x,y: x+y)
opfuncs[0x4] = arith_fn(lambda x,y: x-y)
opfuncs[0x6] = arith_fn(lambda x,y: x*y)
opfuncs[0x20] = cmp_fn(lambda x,y: x > y)
opfuncs[0x22] = cmp_fn(lambda x,y: x < y)
opfuncs[0x50] = lii_op
opfuncs[0x52] = lbi_op
opfuncs[0x54] = pop_op
opfuncs[0x56] = dup_op
opfuncs[0x58] = shf_op
opfuncs[0x5a] = swp_op
opfuncs[0x60] = jmp_op
opfuncs[0x62] = jim_op
opfuncs[0x64] = branch
opfuncs[0x71] = trigger_int

if __name__ == "__main__":
    fname = sys.argv[1]
    f = open(fname, "rb")
    tape = f.read()
    f.close()
    words = unpack_2b(tape)
    vm = Machine(5*1024)
    vm.bind_port(1, sys.stdout)
    vm.copy(words, 0)
    #print(str(vm))
    while vm.halt == False:
        vm.eval()
        #print(str(vm))
    print("Done..") 
