from __future__ import print_function
import re
import collections
from Stack import Stack
import copy

class Cnf:
    def __init__(self, string):
        stringSpace = string.replace('(', '( ', string.count('(')).replace(')', ' )', string.count(')')).replace('~', '~ ', string.count('~'))
        self.opList = stringSpace.split()
        self.prefix = self.to_prefix()
        self.remove_biimplication(self.prefix)
        self.remove_implication(self.prefix)
        self.de_morgan(self.prefix)
        self.fix_literal(self.prefix)
        self.distribution(self.prefix)
        currentList = copy.deepcopy(self.prefix)
        self.distribution(self.prefix)
        while currentList != self.prefix:
            currentList = copy.deepcopy(self.prefix)
            self.distribution(self.prefix)
        self.associate(self.prefix)
        currentList = copy.deepcopy(self.prefix)
        self.associate(self.prefix)
        while currentList != self.prefix:
            currentList = copy.deepcopy(self.prefix)
            self.associate(self.prefix)
        self.clauses = self.getClauseSet(self.prefix)
        self.clausesString = self.getClausesString(self.clauses)
    
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

    def de_morgan(self, components):
        if components[0] == '~':
            literal = components[1]
            if literal[0] == '~':
                del components[:]
                if isinstance(literal[1], str):
                    components.append(literal[1])
                else:
                    for literal1 in literal[1]:
                        components.append(literal1)
                    if len(components) > 1:
                        self.de_morgan(components)
            elif literal[0] == '|':
                del components[:]
                components.append('&')
                for literal1 in literal:
                    if literal1 != '|':
                        components.append(['~', literal1])
            elif literal[0] == '&':
                del components[:]
                components.append('|')
                for literal1 in literal:
                    if literal1 != '&':
                        components.append(['~', literal1])
            
        for literal in components:
                if(len(literal) > 1):
                    self.de_morgan(literal)

    def fix_literal(self,components):
        i = 0
        for comp in components:
            if isinstance(comp, collections.MutableSequence) and len(comp) == 1:
                temp = str(comp[0])
                components[i] = temp
            elif len(comp) > 1:
                self.fix_literal(comp)
            i += 1

    def distribution(self, components):
        if components[0] == '|':
            if len(components[2]) > 1 and components[2][0] == '&':
                operand1 = components[1]
                operand2 = components[2]
                del components[:]
                components.append('&')
                for op in operand2:
                    if op != '&':
                        components.append(['|', operand1, op])
            elif len(components[1]) > 1 and components[1][0] == '&':
                operand1 = components[1]
                operand2 = components[2]
                del components[:]
                components.append('&')
                for op in operand1:
                    if op != '&':
                        components.append(['|', op, operand2])
        for element in components:
            if len(element) > 1:
                self.distribution(element)

    def associate(self, components):
        if(components[0]=="&"):
            temp_components = copy.deepcopy(components)
            del components[:]
            for literal in temp_components:
                if literal=="&":
                    components.append("&")
                else:
                    if literal[0]!="&":
                        components.append(literal)
                    else:
                        for literal_x in literal:
                            if literal_x=="&":
                                continue
                            else:
                                components.append(literal_x)

        if(components[0]=="|"):
            temp_components=copy.deepcopy(components)
            del components[:]
            for literal in temp_components:
                if literal=="|":
                    components.append("|")
                else:
                    if literal[0]!="|":
                        components.append(literal)
                    else:
                        for literal_x in literal:
                            if literal_x=="|":
                                continue
                            else:
                                components.append(literal_x)

        for literal in components:
            if(len(literal)>1):
                self.associate(literal)

    def getClauseSet(self, components):
        clauses = set()
        if components[0] == '&':
            for comp in components:
                if comp != '&':
                    if isinstance(comp,str):
                        negation = '~'+comp
                        if negation in clauses:
                            return set()
                        else:
                            clauses.add(comp)
                    elif len(comp) == 2:
                        if comp[1] in clauses:
                            return set()
                        else:
                            clauses.add(comp[0]+comp[1])
                    else:
                        subclause = frozenset(getClauseSubset(comp))
                        if len(subclause) > 0:
                            clauses.add(subclause)
        elif comp[0] == '|':
            subclause = frozenset(getClauseSubset(comp))
            if len(subclause) > 0:
                clauses.add(subclause)
        elif comp[0] == '~':
            clauses.add(comp[0]+comp[1])          
        return clauses

    def getClausesString(self, clauses):
        clausesList = []
        for clause in clauses:
            if isinstance(clause, str):
                clausesList.append('{' + clause + '}')
            else:
                subsetString = '{'
                subsetString += ', '.join(c for c in clause)
                subsetString += '}'
                clausesList.append(subsetString)
        clausesString = '{'
        clausesString += ', '.join(clausesList) + '}'
        return clausesString

    def printClauses(self):
        print(self.clausesString)


def getClauseSubset(components):
    subclause = set()
    if components[0] == '|':
        for comp in components:
            if comp != '|':
                if isinstance(comp, str):
                    negation = '~'+comp
                    if negation in subclause:
                        return set()
                    else:
                        subclause.add(comp)
                elif len(comp) == 2:
                    if comp[1] in subclause:
                        return set()
                    else:
                        subclause.add(comp[0]+comp[1])
        return subclause

# contoh:
# c = Cnf('~((P2 -> P4) -> (P3 & P4))')
# c.printClauses()     
