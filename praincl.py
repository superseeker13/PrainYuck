#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Basic BF commandline interface
# TODO: Build Gui
import sys
import bfparser as bf

# Causes each comand to be output in detail
debug_mode = True
errheader = 'You Prain Yucked up: '


def main():
    err = False
    if len(sys.argv) == 2:
        prog = bf.readinbf(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-e':
            prog = sys.argv[2]
        elif sys.argv[1] == '-c':
            prog = bf.readinbf(sys.argv[2])
            if bf.syncheck(prog):
                bf.cmpl(prog, 'PrainTest')
                sys.exit(0)
            else:
                print(str(sys.argv[2]) + ': Syntax error')
                err = True
        else:
            print(errheader + 'Unkown flag: ' + sys.argv[2])
            err = True
    else:
        print(errheader + 'Incorrect number of arguments')
        err = True
    if prog != '' and not bf.syncheck(prog):
        print(errheader + 'Unbalanced brackets')
        err = True
    bf.evaluate(prog) if not err else sys.exit(1)


main()
print()
