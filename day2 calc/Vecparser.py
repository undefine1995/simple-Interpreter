#-*coding:utf-8*-

import Veclexer
import ToRPN

class Vecparser:

    def __init__(self, RPN):
        self.list = RPN[:]
        self.stack = []

    def calc(self):
        for item in self.list:
            if item == '+' or item == '-' or item == '*' or item == '/':
                if item == '+':
                    a = self.stack.pop()
                    b = self.stack.pop()
                    s = b + a
                    self.stack.append(s)

                if item == '-':
                    a = self.stack.pop()
                    b = self.stack.pop()
                    s = b - a
                    self.stack.append(s)

                if item == '*':
                    a = self.stack.pop()
                    b = self.stack.pop()
                    s = b * a
                    self.stack.append(s)

                if item == '/':
                    a = self.stack.pop()
                    b = self.stack.pop()
                    s = b / a
                    self.stack.append(s)

            else:
                self.stack.append(item)

        tmp = float(self.stack[0])
        if tmp == int(tmp):
            return int(tmp)
        else:
            return tmp

if __name__ == '__main__':
    while True:
        exp = raw_input('calc>')
        lex = Veclexer.Veclexer(exp)
        t = lex.get_next_token()
        s = ToRPN.ToRPN()
        s.RPN(t)
        while t[0] != 'EOF':
            t = lex.get_next_token()
            s.RPN(t)
        parser = Vecparser(s.list)
        print(parser.calc())