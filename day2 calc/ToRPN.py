#-*coding:utf-8*-

import Veclexer

class ToRPN:
    def __init__(self):
        self.list = []
        self.stack = []

    def RPN(self, token):
        if token[0] != 'EOF':
            if token[0] == 'NUM':
                self.list.append(token[1])
            elif not self.stack:
                self.stack.append(token[1])
            else:
                if token[1] == '+' or token[1] == '-':
                    if self.stack[(len(self.stack)) - 1] == '*' or self.stack[(len(self.stack))-1] == '/':
                        self.list.append(self.stack.pop())
                        self.stack.append(token[1])
                    else:
                        self.stack.append(token[1])
                if token[1] == '*' or token[1] == '/' or token[1] == '(':
                    self.stack.append(token[1])

                if token[1] == ')':
                    while self.stack[(len(self.stack)) - 1] != '(':
                        self.list.append(self.stack.pop())
                    if self.stack[(len(self.stack)) - 1] == '(':
                        self.stack.pop()
        if token[0] == 'EOF':
            while self.stack:
                self.list.append(self.stack.pop())

    def display(self):
        print(self.list)

if __name__ == '__main__':
    exp = '''
        1 + 2 * 3 - (4 - 5) * 6
    '''
    lex = Veclexer.Veclexer(exp)
    t = lex.get_next_token()
    s = ToRPN()
    s.RPN(t)
    while t[0] != 'EOF':
        t = lex.get_next_token()
        s.RPN(t)
    print(s.list)