# Turing Machine

A simple one-tape Turing program interpreter written in Python.

Usage: python TM.py \<program\> "\<tape input\>"

Example: python TM.py prog1.txt "101010110"

The tape alphabet consists of the symbols "0", "1", "#", and " ". States are represented by numbers, with 0 being the halting state and 1 the initial state.

Program files consist of tuples (one per line) describing the transition function of the machine, in the format:

current state, current symbol, new state, new symbol, movement

