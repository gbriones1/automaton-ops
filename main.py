#!/bin/python3

import argparse
import sys

from automaton import Automaton
import operations

OPS = ["union", "intersect", "concat", "kleene_star"]


def check_errors(errors):
    if errors:
        print(f"The automaton is invalid: {errors}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Operation for automatons"
    )
    parser.add_argument("--automaton1", "-a", dest="automaton1", type=str, required=True, help="File of the first automaton description")
    parser.add_argument("--automaton2", "-b", dest="automaton2", type=str, help="File of the second automaton description. Not required for operation kleene_star")
    parser.add_argument("--operation", "-o", dest="operation", type=str, required=True, choices=OPS, help="Operation to execute")
    args = parser.parse_args()
    automaton1 = Automaton(from_file=args.automaton1)
    check_errors(automaton1.errors)
    if args.operation != "kleene_star":
        automaton2 = None
        if args.automaton2:
            automaton2 = Automaton(from_file=args.automaton2)
        else:
            print("Need to define --automaton2")
            sys.exit(1)
        check_errors(automaton2.errors)
        result = getattr(operations, args.operation)(automaton1, automaton2)
    else:
        result = operations.kleene_star(automaton1)
    print(result.render())
    

if __name__ == "__main__":
    main()