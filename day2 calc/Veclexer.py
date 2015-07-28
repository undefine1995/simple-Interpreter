#-*coding:utf-8*-

NUM, ADD, SUB, MUL, DIV, LBRACK, RBRACK, EOF = 'NUM', 'ADD', 'SUB', 'MUL', 'DIV', 'LBRACK', 'RBRACK', 'EOF'

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


class  Veclexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('输入有误')

    def advance(self):
        self.pos += 1

        if self.pos > (len(self.text)-1):
            self.current_char = None

        else:
            self.current_char = self.text[self.pos]

    def get_num(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        try:
            return float(result)
        except Exception as e:
            self.error()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = (NUM, self.get_num())
                return token

            if self.current_char == '+':
                token = (ADD, self.current_char)
                self.advance()
                return token

            if self.current_char == '-':
                token = (SUB, self.current_char)
                self.advance()
                return token

            if self.current_char == '*':
                token = (MUL, self.current_char)
                self.advance()
                return token

            if self.current_char == '/':
                token = (DIV, self.current_char)
                self.advance()
                return token

            if self.current_char == '(':
                token = (LBRACK, self.current_char)
                self.advance()
                return token

            if self.current_char == ')':
                token = (RBRACK, self.current_char)
                self.advance()
                return token


            self.error()

        return (EOF, 'EOF')



if __name__ == '__main__':  
    exp = '''
        2+5.5-(8*5/3)
    '''  
    lex = Veclexer(exp)  
    t = lex.get_next_token()

    while t[1] != 'EOF':
        print(t)
        t = lex.get_next_token()