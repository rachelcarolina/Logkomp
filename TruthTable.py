from __future__ import print_function
from itertools import product
from Stack import Stack
import re

class TruthTable:
      def __init__(self, string):
            stringSpace = string.replace('(', '( ', string.count('(')).replace(')', ' )', string.count(')')).replace('~', '~ ', string.count('~'))
            opList = stringSpace.split()
            self.varList = []
            self.value = Stack()
            self.ops = Stack()
            self.resultList = []
            for op in opList:
                  if op.isupper() or op.islower():
                        self.varList.append(op)
            self.varList = list(set(self.varList))
            self.varList.sort()
            varNumber = len(self.varList)
            self.valueList = list(product((0,1), repeat=varNumber))
            for values in self.valueList:
                  dict = {}
                  for var in self.varList:
                        dict[var] = values[self.varList.index(var)]
                  i = 0
                  while i < len(opList):
                        op = opList[i]
                        if op.isupper() or op.islower():
                              self.value.push(dict[op])
                              i += 1
                        elif op == '(' or op == '->' or op == '&' or op == '|' or op == '<->':
                              self.ops.push(op)
                              i += 1
                        elif op == '~':
                              if opList[i+1] != '(' and opList[i+1] != '~':
                                    op = opList[i+1]
                                    self.value.push(self.negation(dict[op]))
                                    i += 2
                                    while self.ops.peek() == '~':
                                          op = self.value.pop()
                                          self.value.push(self.negation(op))
                              else:
                                    self.ops.push(op)
                                    i += 1
                        elif op == ')':
                              while not self.ops.isEmpty() and self.ops.peek() != '(':
                                    currentOp = self.ops.pop()
                                    operand2 = self.value.pop()
                                    operand1 = self.value.pop()
                                    self.value.push(self.evaluate(operand1, operand2, currentOp))
                              self.ops.pop()
                              i += 1
                              
                  while not self.ops.isEmpty():
                        print(hehe)
                        currentOp = self.ops.pop()
                        if currentOp == '~':
                              operand = self.value.pop()
                              self.value.push(self.negation(operand))
                        else:
                              operand2 = self.value.pop()
                              operand1 = self.value.pop()
                              self.value.push(self.evaluate(operand1, operand2, currentOp))
                  self.resultList.append(self.value.pop())

      def evaluate(self, operand1, operand2, operator):
            if operator == '|':
                  return self.disjunction(operand1, operand2)
            elif operator == '&':
                  return self.conjunction(operand1, operand2)
            elif operator == '->':
                  return self.implication(operand1, operand2)
            elif operator == '<->':
                  return self.biimplication(operand1, operand2)

      def negation(self, operand):
            if operand == 0:
                  return 1
            return 0

      def conjunction(self, operand1, operand2):
            if operand1 and operand2:
                  return 1
            return 0
      
      def disjunction(self, operand1, operand2):
            if operand1 or operand2:
                  return 1
            return 0

      def implication(self, operand1, operand2):
            if operand1 == 1 and operand2 == 0:
                  return 0
            return 1
      
      def biimplication(self, operand1, operand2):
            if operand1 == 0 and operand2 == 0:
                  return 1
            elif operand1 == 1 and operand2 == 1:
                  return 1
            return 0
      
      def printTt(self):
            size = len(self.valueList)
            varNumber = len(self.varList)
            for i in range(0, varNumber):
                  print(self.varList[i], end='\t')
            print('F')
            for i in range(0, size):
                  for j in range(0, varNumber):
                        print(self.valueList[i][j], end='\t')
                  print(self.resultList[i])
