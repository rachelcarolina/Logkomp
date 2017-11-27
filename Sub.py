from __future__ import print_function
import re
import collections
from Stack import Stack
import copy

class Sub:
    def __init__ (self, string):
        stringSpace = string.replace('(', '( ', string.count('(')).replace(')', ' )', string.count(')')).replace('~', '~ ', string.count('~'))
        self.opList = stringSpace.split()
        self.prefix = self.to_prefix()
        self.remove_biimplication(self.prefix)
        self.remove_implication(self.prefix)
        self.subList = []
        self.get_subList(self.prefix)



    def to_prefix(self):
        operators = Stack()
        operands = Stack()
        i = len(self.opList) - 1
        while i >= 0:
            if self.opList[i] == ')' or self.opList[i] == '&' or self.opList[i] == '|' or self.opList[i] == '->' or self.opList[i] == '<->':
                operators.push(self.opList[i])
            elif self.opList[i].islower() or self.opList[i].isupper():
                operands.push(self.opList[i])
            elif self.opList[i] == '~':
                currentList = [self.opList[i], operands.pop()]
                operands.push(currentList)
            elif self.opList[i] == '(':
                currentList = []
                if not operators.isEmpty() and operators.peek() != ')':
                    currentList.append(operators.pop())
                operators.pop()
                currentList.append(operands.pop())
                currentList.append(operands.pop())
                operands.push(currentList)
            i -= 1
        return operands.pop()

    def remove_biimplication(self, components):
        if (components[0] == '<->'):
           operand1 = components[1]
           operand2 = components[2]
           components[0] = '&'
           components[1] = ['->', operand1, operand2]
           components[2] = ['->', operand2, operand1]
        for operand in components:
            if(len(operand) > 1):
                self.remove_biimplication(operand)
    
    def remove_implication(self, components):
        if components[0] == '->':
            operand1 = components[1]
            components[0] = '|'
            components[1] = ['~', operand1]
        for operand in components:
            if(len(operand) > 1):
                self.remove_implication(operand)

    def get_subList(self, components):
        if isinstance(components, str):
            self.subList.append(components)
        elif components[0] == '~':
            self.subList.append(components)
            self.get_subList(components[1])
        elif components[0] == '&' or components[0] == '|':
            self.subList.append(components)
            self.get_subList(components[1])
            self.get_subList(components[2])
        
    def to_infix(self, sub):
        if isinstance(sub, str):
           return sub
        elif len(sub) == 2:
            operand = self.to_infix(sub[1])
            return "~{0}".format(operand)
        elif len(sub) > 2:
           operator = sub[0]
           operand1 = self.to_infix(sub[1])
           operand2 = self.to_infix(sub[-1])
           return "({0} {1} {2})".format(operand1, operator, operand2)
    
    def print_subList(self, string):
        for sub in self.subList:
            print(self.to_infix(sub))
        print("{0} has {1} different subformulas".format(string, len(self.subList)))
        
        

# s = Sub('~((P2 -> P4) -> (P3 & P4))')
