import operators as op

# Stack Ops
def lbi_op(vm, arg):
    imm = vm.readword()
    vm.push(imm)

def lii_op(vm, arg):
    vm.push(arg)

def pop_op(vm, arg):
    v = vm.pop()
    vm.port[arg].write(str(v)+"\n")

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

def define_stack_ops(t):
    t[op.LLI]=lii_op
    t[op.LBI]=lbi_op
    t[op.POP]=pop_op
    t[op.DUP]=dup_op
    t[op.SHF]=shf_op
    t[op.SWP]=swp_op

# Control Ops
def branch_stack(vm, arg):
    vm.popa()
    vm.popb()
    if vm.b != 0:
        if arg == 0:
            vm.pc = vm.a
        else:
            vm.pc += vm.a

def branch_imm(vm, arg):
    vm.popa()
    v = vm.readword()
    if vm.a != 0:
        if arg == 0:
            vm.pc = v
        else:
            vm.pc += v

def jump_stack(vm, arg):
    vm.popa()
    if arg == 0:
        vm.pc = vm.a
    else:
        vm.pc += vm.a

def jump_imm(vm, arg):
    tgt = vm.readword()
    if arg == 0:
        vm.pc = tgt
    else:
        vm.pc += tgt-1

def define_control_ops(t):
    t[op.JMP]=jump_stack
    t[op.JIM]=jump_imm
    t[op.BX]=branch_stack
    t[op.BI]=branch_imm

