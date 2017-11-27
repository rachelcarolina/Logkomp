import sys
from TruthTable import TruthTable
from Sub import Sub
from Cnf import Cnf

class main:
    def __init__(self):
        number = raw_input()
        for i in range(0, int(number)):
            line = raw_input()
            doCommand(line)
    
def doCommand(operation):
    if operation[0:2] == 'tt':
        sentence = operation[3:]
        tt = TruthTable(sentence)
        tt.printTt()
    if operation[0:3] == 'sub':
        sentence = operation[4:]
        sub = Sub(sentence)
        sub.print_subList(sentence)
    if operation[0:4] == 'ecnf':
        sentence = operation[5:]
        cnf = Cnf(sentence)
        cnf.printClauses()

main()
