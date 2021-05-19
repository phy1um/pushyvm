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
from argparse import ArgumentParser

parser = ArgumentParser(description="Simple VM Bytecode Interpreter")
parser.add_argument("-v", dest="verbose", action='store_true')
parser.add_argument("-i", dest="inter", action='store_true')
parser.add_argument("file", type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    f = open(args.file, "rb")
    tape = f.read()
    f.close()
    program = unpack_2b(tape)
    vm = Machine(5*1024)
    vm.bind_port(1, sys.stdout)
    vm.copy(program, 0)
    vm.interractive = args.inter
    opfuncs = {}
    define_std_env(opfuncs)
    if args.verbose:
        print(str(vm))
    while vm.halt == False:
        vm.eval(opfuncs, verbose=args.verbose)
        if args.verbose:
            print(str(vm))
    if args.verbose:
        print("Done") 
    sys.exit(vm.exit_status)


