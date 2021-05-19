from svm import Machine, unpack_2b, define_sys_ops
from numbers import define_arithmetic_ops, define_comparison_ops, define_bitwise_ops
from logic import define_control_ops, define_stack_ops


def define_std_env(t):
    define_arithmetic_ops(t)
    define_comparison_ops(t)
    define_bitwise_ops(t)
    define_control_ops(t)
    define_stack_ops(t)
    define_sys_ops(t)

import sys

if __name__ == "__main__":
    fname = sys.argv[1]
    f = open(fname, "rb")
    tape = f.read()
    f.close()
    words = unpack_2b(tape)
    vm = Machine(5*1024)
    vm.bind_port(1, sys.stdout)
    vm.copy(words, 0)
    opfuncs = {}
    define_std_env(opfuncs)
    #print(str(vm))
    while vm.halt == False:
        vm.eval(opfuncs)
        #print(str(vm))
    print("Done..") 


