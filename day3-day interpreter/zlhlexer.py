#-*coding:utf-8*-

VAR, MAIN, PRINT, SEM, EOF, LBOUND, RBOUND, QU ,ID= 'VAR', 'MAIN', 'PRINT', 'SEM', 'EOF', 'LBOUND', 'RBOUND', 'QU', 'ID'
ADD, SUB, MUL, DIV, LBRACK, RBRACK = 'ADD', 'SUB', 'MUL', 'DIV', 'LBRACK', 'RBRACK'
INT, FLOAT, CHAR = 'INT', 'FLOAT', "CHAR"
AS = 'AS'

class Veclexer:

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
           tmp = float(result)
        except Exception as e:
            self.error()

        if tmp == int(tmp):
            return (INT,int(result))
        else:
            return (FLOAT,float(result))

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_char(self):
        self.advance()
        result = self.current_char
        self.advance()
        return result


    def _print(self):
        n = self.text[self.pos  : self.pos + 5]
        if n == 'print':
            self.pos += 5
            self.current_char = self.text[self.pos]

            return (PRINT, 'print')

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        return (ID,result)


    def _var(self):
        n = self.text[self.pos  : self.pos + 5]
        if n == 'float':
            self.pos += 5
            self.current_char = self.text[self.pos]

            return (VAR, 'float')

        if n[0:3] == 'int':
            self.pos += 3
            self.current_char = self.text[self.pos]

            return (VAR, 'int')

        if n[0:5] == 'chars':
            self.pos += 5
            self.current_char = self.text[self.pos]

            return (VAR, 'chars')

    def _main(self):
        n = self.text[self.pos  : self.pos + 4]
        if n == 'main':
            self.pos += 4
            self.current_char = self.text[self.pos]

            return (MAIN, 'main')

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = self.get_num()
                return token

            if self.current_char.isalpha():
                token = self._main()
                if not token:
                    token = self._var()
                if not token:
                    token = self._print()
                return token if token else self._id()

            if self.current_char == '=':
                token = (AS, self.current_char)
                self.advance()
                return token

            if self.current_char == '{':
                token = (LBOUND, self.current_char)
                self.advance()
                return token

            if self.current_char == '}':
                token = (RBOUND, self.current_char)
                self.advance()
                return token

            if self.current_char == ';':
                token = (SEM, self.current_char)
                self.advance()
                return token

            if self.current_char == '\'':
                token = (CHAR, self.get_char())
                self.advance()
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


    def has_next(self):
        return self.current_char != EOF


if __name__ == '__main__':
    exp = '''
        main{
        int i;
        chars aa;
        i=5;
        a='b';
        a=a+5;
        print a;
        }

    '''
    lex = Veclexer(exp)
    t = lex.get_next_token()

    while t[0] != EOF:
        print(t)
        print(lex.has_next())
        t = lex.get_next_token()