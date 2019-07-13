#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Basic BF parser for PrainYuck
from datetime import datetime
import sys
import os
import platform

debug_mode = True
errheader = 'You Prain Yucked up: '
# Reads in program and checks for syntax errors


def readinbf(fname):
    if '.bf' in fname or '.b' in fname:
        try:
            f = open(fname, 'r')
            prg = f.read()
            f.close()
            # Removes unnessacary characters
            commands = ['<', '>', '+', '-', '.', ',', '[', ']']
            prg = [x for x in prg if x in commands]
            return prg
        except e:
            print('File read error.')
            print('Exiting to shell...')
            sys.exit(1)
    else:
        fileext = fname.split('.')[-1]
        print(errheader + 'Invalid file extension *.' + fileext)
        print('Exiting to shell...')
        sys.exit(1)

# Check if program is valid


def syncheck(prg):
    lbracket = 0
    rbracket = 0
    for x in prg:
        if x == '[':
            lbracket += 1
        elif x == ']':
            rbracket += 1
    return lbracket == rbracket


def evaluate(prg):
    if debug_mode:
        bugout = open('bf_debug.txt', 'w+')
        bugout.write("Prain Yuck Trace: {}\n".format(str(sys.argv[1::])))
        bugout.write('Compile time: {} \n\n'.format(str(datetime.now())))

    num = 0
    prgPos = 0
    memPos = 0
    mem = [0] * (prg.count('>') * 2)

    while prgPos < len(prg) - 1:
        # increment the data pointer
        if '>' == prg[prgPos]:
            memPos += 1
        # decrement the data pointer
        elif '<' == prg[prgPos]:
            memPos -= 1
        # increment the byte at the data pointer.
        elif '+' == prg[prgPos]:
            mem[memPos] += 1 if mem[memPos] < 255 else -255
        # decrement the byte at the data pointer.
        elif '-' == prg[prgPos]:
            mem[memPos] -= 1 if mem[memPos] > 0 else -255
        # output the byte at the data pointer.
        elif '.' == prg[prgPos]:
            try:
                strout = str(chr(mem[memPos]))
                print(strout, end='')
            except e:
                print('Runtime I/O error.')
                print("\t" + str(sys.exc_info()[0]))
                if !debug_mode:
                    print("Try rerunning in debug mode for trace \n")
                sys.exit(1)

        # Accept one byte of input,
        # storing its value in the byte at the data pointer
        elif ',' == prg[prgPos]:
            mem[memPos] = sys.stdin.read(1)

        # Beginning of while

        elif '[' == prg[prgPos]:
            if mem[memPos] == 0:
                brace = 1
                while brace > 0:
                    prgPos += 1
                    if prg[prgPos] == '[':
                        brace += 1
                    elif prg[prgPos] == ']':
                        brace -= 1
        # End of while
        elif ']' == prg[prgPos]:
            brace = 1
            while brace > 0:
                prgPos -= 1
                if prg[prgPos] == '[':
                    brace -= 1
                elif prg[prgPos] == ']':
                    brace += 1
            prgPos -= 1

        # Increment program counter
        prgPos += 1

        # Output
        if debug_mode:
            try:
                num += 1
                bugout.write('{:3}: '.format(num))
                bugout.write('PrgPosition: {:4} '.format(str(prgPos)))
                bugout.write('MemPosition: {:4} '.format(str(memPos)))
                bugout.write('Command: {:4} '.format(str(prg[prgPos])))
                bugout.write('Mem Contents: {:4} \n'.format(str(mem[memPos])))
            except IndexError as e:
                print('Command #{:4} \n'.format(str(prgPos)))
                print('\nRuntime debug error')
                print ("\tIndexError: index out of range.")
                sys.exit(1)
    bugout.close()


def cmpl(prg, fname):
    # Create c file
    fout = open(fname + ".c", 'w+')

    # Set up string
    cstr = "#include <stdio.h>\n"
    cstr += "void main(){\n"
    cstr += "\tchar arr[256] = {0};\n"
    cstr += "\tchar *ptr=arr;\n"

    index = 0
    indent = 1
    while index < len(prg):
        cstr += "\t" * indent

        # increment the data pointer
        if '>' == prg[index]:
            if prg[index+1] != '>':
                cstr += "ptr++;"
            else:
                count = 1
                while prg[index+1] == '>':
                    index += 1
                    count += 1
                cstr += "ptr += {};".format(count)

        # decrement the data pointer
        elif '<' == prg[index]:
            if prg[index+1] != '<':
                cstr += "ptr--;"
            else:
                count = 1
                while prg[index+1] == '<':
                    index += 1
                    count += 1
                cstr += "ptr -= {};".format(count)

        # increment the byte at the data pointer.
        elif '+' == prg[index]:
            if prg[index+1] != '+':
                cstr += "*ptr++;"
            else:
                count = 1
                while prg[index+1] == '+':
                    index += 1
                    count += 1
                cstr += "*ptr += {};".format(count)

        # decrement the byte at the data pointer.
        elif '-' == prg[index]:
            if prg[index+1] != '-':
                cstr += "*ptr--;"
            else:
                count = 1
                while prg[index+1] == '-':
                    index += 1
                    count += 1
                cstr += "*ptr -= {};".format(count)

        # output the byte at the data pointer.
        elif '.' == prg[index]:
            cstr += "printf(\"%c\",*ptr);"

        # Accept one byte of input,
        # storing its value in the byte at the data pointer
        elif ',' == prg[index]:
            cstr += "*ptr = getchar();"

        # Beginning of while
        elif '[' == prg[index]:
            cstr += "while (*ptr) {"
            indent += 1

        # End of while
        elif ']' == prg[index]:
            cstr += "}"
            indent -= 1

        # Add new newline after each command
        cstr += "\n"
        index += 1

    # Write and close file
    cstr += "\treturn;\n}"
    fout.write(cstr)
    fout.close()

    # Bash gcc compilation
    if 'Windows' not in platform.system():
        os.system("gcc -c " + fname + ".c" + " > cmplout.txt")
        os.system("gcc -o {} {}.o".format(fname, fname))
