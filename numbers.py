import svm
import operators as op

def arith_fn(f):
    def op(vm, arg):
        vm.popa()
        vm.popb()
        vm.push(f(vm.a, vm.b))
    return op

def cmp_fn(f):
    def op(vm, arg):
        vm.popa()
        vm.popb()
        if f(vm.a, vm.b):
            vm.push(1)
        else:
            vm.push(0)
    return op

def op_not(vm, arg):
    vm.popa()
    if vm.a != 0:
        vm.push(0)
    else:
        vm.push(1)

def arg_fn(f):
    def op(vm, arg):
        vm.popa()
        f(vm.a, arg)
    return op

def define_arithmetic_ops(t):
    t[op.ADD] = arith_fn(lambda x,y: x+y)
    t[op.SUB] = arith_fn(lambda x,y: x-y)
    t[op.MUL] = arith_fn(lambda x,y: x*y)
    t[op.DIV] = arith_fn(lambda x,y: x//y)
    t[op.MOD] = arith_fn(lambda x,y: x%y)

def define_comparison_ops(t):
    t[op.LT] = cmp_fn(lambda x,y: x < y)
    t[op.LTE] = cmp_fn(lambda x,y: x <= y)
    t[op.GT] = cmp_fn(lambda x,y: x > y)
    t[op.GTE] = cmp_fn(lambda x,y: x >= y)
    t[op.EQ] = cmp_fn(lambda x,y: x == y)
    t[op.NEQ] = cmp_fn(lambda x,y: x != y)
    
def define_bitwise_ops(t):
    t[op.AND] = arith_fn(lambda x,y: x&y)
    t[op.OR] = arith_fn(lambda x,y: x|y)
    t[op.XOR] = arith_fn(lambda x,y: x ^ y)
    t[op.NOT] = op_not
    t[op.SHL] = arg_fn(lambda x, y: x << y)
    t[op.SHR] = arg_fn(lambda x, y: x >> y)

