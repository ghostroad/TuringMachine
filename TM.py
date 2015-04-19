# Author: Mushfeq Khan
# Date: 4/15/2015

import sys, time


ALPHABET = ["0", "1", " ", "#"]
HALT_STATE = 0
INIT_STATE = 1
MOVEMENTS = ["L", "R"]
DELAY = 0.05


class Parser:
    def __init__(self):
        self.transition_function = {}
    def raise_parse_exception(self, message, line):
        raise ValueError(message + "\nInput line: %s" % line)
    def validate(self, entries, line):
        if (len(entries) != 5):
            self.raise_parse_exception("Invalid number of entries", line)
        curr_state, curr_symb, new_state, new_symb, movement = entries
        if (curr_symb not in ALPHABET):
            self.raise_parse_exception("Current symbol \"%s\" not in alphabet" % curr_symb, line)
        if (new_symb not in ALPHABET):
            self.raise_parse_exception("New symbol \"%s\" not in alphabet" % new_symb, line)
        if (movement not in MOVEMENTS):
            self.raise_parse_exception("Invalid movement \"%s\"" % movement, line)
        try:
            curr_state = int(curr_state)
            if curr_state <= 0:
                raise ValueError
        except ValueError, e:
            self.raise_parse_exception("Invalid current state: %s" % curr_state, line)
        try:
            new_state = int(new_state)
            if new_state < 0:
                raise ValueError
        except ValueError, e:
            self.raise_parse_exception("Invalid new state: %s" % new_state, line)

        if self.transition_function.has_key((curr_state, curr_symb)):
            self.raise_parse_exception("Conflicting entry in transition function", line)
        else:
            self.transition_function[(curr_state, curr_symb)] = (new_state, new_symb, movement)
    def parse(self, filename):
        for line in open(filename).readlines():
            entries = line.strip().split(",")
            self.validate(entries, line)



class TuringMachine:
    def __init__(self, tape=[], transition_function ={}):
        self.tape = tape
        self.curr_state = INIT_STATE
        self.num_steps = 0
        self.head_position = 0
        self.transition_function = transition_function
        self.hung = False
    def halted(self):
        return self.curr_state == HALT_STATE
    def print_status(self):
        print "".join(self.tape)
        print self.head_position * " " + "^"
        print "%s steps, state %s" % (self.num_steps, self.curr_state)
        if self.halted(): 
            print "Halted."
        if self.hung: 
            print "Hung."
        print

    def run_single_step(self):
        if self.hung or self.halted():
            return
        if len(self.tape) <= self.head_position:
            self.tape.append(" ")
        curr_symb = self.tape[self.head_position]
        source = (self.curr_state, curr_symb)
        if (self.transition_function.has_key(source)):
            new_state, new_symb, movement = self.transition_function[source]
            self.curr_state = new_state
            self.tape[self.head_position] = new_symb
            if (movement == "R"): self.head_position += 1
            if (movement == "L" and self.head_position > 0): self.head_position -= 1
            self.num_steps += 1
            self.print_status()
        else:
            self.hung = True
            self.print_status()

    def run(self):
        self.print_status()
        while (not (self.halted() or self.hung)):
            self.run_single_step()
            time.sleep(DELAY)

    def run_some(self, steps):
        self.print_status()
        for i in range(steps):
            self.run_single_step()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise RuntimeError("Usage: python TM.py <program.txt> \"<tape input>\"")
    program_file = sys.argv[1]
    tape_input = sys.argv[2]
    if not all(symbol in ALPHABET for symbol in tape_input):
        raise ValueError("Invalid tape input")

    parser = Parser()
    parser.parse(program_file)

    machine = TuringMachine(list(tape_input), parser.transition_function)
    
    while True:
        num_steps = raw_input("Number of steps to run (q to quit, 0 to run till halted): ")
        if num_steps == "q":
            break
        try:
            num_steps = int(num_steps)
            if num_steps < 0:
                raise ValueError
            if num_steps == 0:
                machine.run()
            else:     
                machine.run_some(num_steps)
        except ValueError, e:
            print "Invalid input"
    




