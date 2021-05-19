import operators as op
import struct

def unpack_2b(b):
    n = len(b) // 2
    fmt = f">{n}h"
    return struct.unpack(fmt, b)

def get_op(d):
    return (d&0xff00) >> 8

def get_arg(d):
    return d&0xff

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
        self.interractive = False
        self.exit_status = 1

    def bind_port(self, i, f):
        self.port[i] = f

    def init_memory(self, m):
        self.ram = [0]*m
        self.sp = m-1

    def copy(self, words, to):
        for i,w in enumerate(words):
            self.ram[to+i] = w 

    def eval(self, opfuncs, verbose=False):
        cmd = self.readword()
        op = get_op(cmd)
        arg = get_arg(cmd)
        if verbose:
            print(f"Eval {op:#x}[{arg:#x}]")
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

def trigger_int(vm, arg):
    if arg == 0:
        vm.halt = True
        vm.exit_status = 0
    elif arg == 1:
        prompt = ""
        if vm.interractive:
            prompt = "> "
        s = input(prompt) 
        v = int(s)
        vm.push(v)
    else:
        print("INVALID INTERRUPT: " + str(arg))
        vm.halt = True

def define_sys_ops(t):
    t[op.INT] = trigger_int

