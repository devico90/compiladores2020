
# Author: Christiano Braga
# http://github.com/ChristianoBraga

import tatsu                            # Tatsu is the parser generator.
# Impiler is the compiler from Imπ to π IR.
from impiler import Impiler
# pi is the Python implementation of the π framework
from pi import run
import sys
import traceback
import getopt           # System and command line modules.
from pillvm import pi_llvm, pi_llvm_jit
import pprint


def print_help():
    print('Imπ2 compiler, June 2020')
    print('http://github.com/ChristianoBraga/PiFramework')
    print(
        'imp2.py -f <impfile> [-s | -a | -d | -p | -t | --at | --pt | --stats | --state n | --last n | --llvm | llvm_jit]')
    print('-s : Prints source code.')
    print('-a : Prints syntax tree.')
    print('-d : Prints parse trace.')
    print('-p : Prints Π IR abstract syntax tree.')
    print('-t : Prints full Π automaton evaluation trace.')
    print('--at : Prints the syntax tree and terminates.')
    print('--pt : Prints Π IR abstract syntax tree and terminates.')
    print('--stats : Prints execution statistics.')
    print('--state n : Prints the nth state of the automaton.')
    print('--last n : Prints the (last - n)th state of the automaton.')
    print('--llvm : Prints LLVM code.')
    print('--llvm_jit : Runs LLVM JIT code.')


def main(argv):
    source = ''
    print_ast = False
    print_parse_trace = False
    print_pilib_ast = False
    print_source = False
    print_trace = False
    print_stats = False
    print_state = False
    print_last = False
    print_llvm = False
    run_llvm_jit = False
    terminate = False
    display_state = 0
    last_n_state = 0

    try:
        opts, args = getopt.getopt(
            argv, "f:sapte", ['at', 'pt', 'llvm', 'llvm_jit', 'stats', 'state=', 'last='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-f':
            source = open(arg).read()
        elif opt == '-s':
            print_source = True
        elif opt == '-a':
            print_ast = True
        elif opt == '-d':
            print_parse_trace = True
        elif opt == '-p':
            print_pilib_ast = True
        elif opt == '-t':
            print_trace = True
        elif opt == '--at':
            print_ast = True
            terminate = True
        elif opt == '--pt':
            print_pilib_ast = True
            terminate = True
        elif opt == '--stats':
            print_stats = True
        elif opt == '--state':
            print_state = True
            display_state = int(arg)
        elif opt == '--last':
            print_last = True
            last_n_state = int(arg)
        elif opt == '--llvm':
            print_llvm = True
        elif opt == '--llvm_jit':
            run_llvm_jit = True

    if not source:
        print_help()
        exit(2)

    if print_source:
        print('Imπ source code: ')
        print(source)

    imp_grammar = open('imp2.ebnf').read()

    if print_parse_trace:
        parser = tatsu.compile(imp_grammar, trace=True, colorize=True)
    else:
        parser = tatsu.compile(imp_grammar)

    if print_ast:
        try:
            ast = parser.parse(source)
            print(ast)
            exit(1)
            print('Concrete syntax tree: ')
            pprint.pprint(ast, indent=2, width=20)
            if terminate:
                exit(1)
            print()
        except Exception as e:
            print('Parser error: ' + str(e))
            exit(2)

    try:
        pi_ast = parser.parse(source, semantics=Impiler())
        if print_pilib_ast:
            print('π IR syntax tree:')
            pprint.pprint(pi_ast, indent=2, width=20)
            print()
        if terminate:
            exit(1)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('Imπ compilation error: ')
        tbl = traceback.format_exception(exc_type, exc_value, exc_traceback)
        imp_tb = [e for e in tbl if 'PiFramework' in e]
        for ex in imp_tb:
            print(ex)
        print(exc_value)
        exit(2)

    try:
        (tr, ns, dt) = run(pi_ast)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('Imπ evaluation error: ')
        tbl = traceback.format_exception(exc_type, exc_value, exc_traceback)
        imp_tb = [e for e in tbl if 'PiFramework' in e]
        for ex in imp_tb:
            print(ex)
        print(exc_value)
        exit(2)

    if print_llvm or run_llvm_jit:
        module = pi_llvm(pi_ast)
        if print_llvm:
            print(module)
        if run_llvm_jit:
            pi_llvm_jit(module)
    else:
        if print_trace:
            for state_number in range(len(tr)):
                print('State #' + str(state_number) + ' of the π automaton:')
                print(tr[state_number])
        else:
            if print_last:
                display_state = len(tr) - (last_n_state + 1)
            else:
                display_state = len(tr) - 1
            print('State #' + str(display_state) + ' of the π automaton:')
            print(tr[display_state])

        if print_stats:
            print('Number of evaluation steps:', ns)
            print('Evaluation time:', dt)


if __name__ == '__main__':
    main(sys.argv[1:])
