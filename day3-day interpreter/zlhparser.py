#-*utf-8*-
import zlhlexer


#不涉及控制语句 未生成语法树
class zlhparser:
    '''
    LL(1) parser.
    '''

    def __init__(self, lexer):
        self.lexer = lexer

        self.pos = 0
        self.cur_token = lexer[self.pos]
        #save as {a['int',1]} 满足语义分析要求
        self.symtab = {} 

    def _main(self):
        if self.lexer[0][0] != zlhlexer.MAIN and self.lexer[0][1] != '{' and self.lexer[len(self.lexer)-1][1] != '}':
            raise Exception('main{}?')
        else:
            self.pos = 2
            self.cur_token = self.lexer[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > (len(self.lexer)-1):
            self.cur_token = None

        else:
            self.cur_token = self.lexer[self.pos]
    def  parser(self):
        if self.pos == 0:
            self._main()
            self.stat()
        else:
            raise Exception('something error:pos not begin with zero')

    def stat(self):
        #print self.cur_token
        if self.match(zlhlexer.VAR):
            while self.cur_token[0] == zlhlexer.VAR:
                val = self.cur_token[1]

                self.advance()

                if self.match(zlhlexer.ID):
                    self.symtab[self.cur_token[1]] = [val]
                    #print self.symtab
                    self.advance()

                if not self.match(zlhlexer.SEM):
                    raise Exception(';?')
                else:
                    self.advance()
        else:
            raise Exception('Sequence error')

        if self.match(zlhlexer.ID):
        # Asignment
            while self.cur_token[0] == zlhlexer.ID:
                t = self.cur_token[1]
                #print t
                self.advance()

                if self.match(zlhlexer.AS):
                    self.advance()
        
                    self.symtab[t].append(self.cur_token[1])
                    #print self.symtab
                    self.advance()

                if not self.match(zlhlexer.SEM):
                    raise Exception(';?')
                else:
                    self.advance()

        else:
            raise Exception('Sequence error')

        if self.match(zlhlexer.PRINT):
        # print statement
            while self.cur_token[0] == zlhlexer.PRINT:
                self.advance()
                if self.match(zlhlexer.ID):
                    tmp = self.cur_token[1]
                    try:
                        print self.symtab[tmp][1]
                    except Exception as e:
                        raise Exception('not Assignment')
                    self.advance()
                if not self.match(zlhlexer.SEM):
                    raise Exception(';?')
                else:
                    self.advance()

        else:
            raise Exception('Sequence error')


    def expr(self):
        token_type, token_val = self.cur_token
        if token_type == zlhlexer.CHAR:
            self.advance()
            return token_val
        if token_type == zlhlexer.INT:
            tmp = ''
            while cur_token[1] != ';':
                tmp += self.cur_token[1]
                self.advance()
            val = eval(tmp)
            return val
        if token_type == zlhlexer.FLOAT:
            self.advance()
            return token_val


    def match(self, token_type):
        if self.cur_token[0] == token_type:
            return True
        

if __name__ == '__main__':
    prog = '''
    main{
        int a;
        float b;
        a = 1;
        b = 1.1;
        print b;
    }
    '''
    undefine = []
    lex = zlhlexer.Veclexer(prog)
    t = lex.get_next_token()

    while t[0] != zlhlexer.EOF:
        undefine.append(t)
        t = lex.get_next_token()
    print undefine
    parser = zlhparser(undefine)
    parser.parser()