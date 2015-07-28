#-*coding:utf-8*-

INTEGER, ADD, SUB, MUL, DIV, EOF = 'INTEGER', 'ADD', 'SUB', 'MUL', 'DIV', 'EOF'


class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __srt__(self):
        return '({type}, {value})'.format(
                type = self.type,
                value = self.value
            )

    def __repe__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('输入有误')

    def advance(self):
        self.pos += 1

        if self.pos > (len(self.text)-1):
            self.current_char = None

        else:
            self.current_char = self.text[self.pos]

    def get_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = Token(INTEGER,self.get_int())
                return token

            if self.current_char == '+':
                token = Token(ADD,self.current_char)
                self.advance()
                return token

            if self.current_char == '-':
                token = Token(SUB,self.current_char)
                self.advance()
                return token

            if self.current_char == '*':
                token = Token(MUL,self.current_char)
                self.advance()
                return token

            if self.current_char == '/':
                token = Token(DIV,self.current_char)
                self.advance()
                return token

            self.error()

        return Token(EOF, None)


    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        #self.current_token = self.get_next_token()
        op = self.current_token
        if op.type == ADD:
            self.eat(ADD)
        if op.type == SUB:
            self.eat(SUB)
        if op.type == MUL:
            self.eat(MUL)
        if op.type == DIV:
            self.eat(DIV)

        #self.current_token = self.get_next_token()
        right = self.current_token
        self.eat(INTEGER)

        if op.type == ADD:
            result = left.value + right.value
        if op.type == SUB:
            result = left.value - right.value
        if op.type == MUL:
            result = left.value * right.value
        if op.type == DIV:
            result = left.value / right.value

        return result

def main():
    while True:
        try:
            text = raw_input('input>')

        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()

        print result

if __name__ == '__main__':
    main()