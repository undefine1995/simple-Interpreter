#-*coding:utf-8*-
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
                    if len(self.symtab[t]) == 1:
                        self.symtab[t].append(self.expr())
                    elif len(self.symtab[t]) == 2:
                        self.symtab[t][1] = self.expr()
                    #print self.symtab

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
        tmp = []
        while self.cur_token and self.cur_token[1] != ';':
            tmp.append(self.cur_token)
            self.advance()

        sets = set()
        for item in tmp:
            sets.add(item[0])

        if len(tmp) == 1:
            if tmp[0][0] == zlhlexer.ID:
                return self.symtab[tmp[0][1]][1]
            if tmp[0][0] != zlhlexer.ID:
                return tmp[0][1]

        elif zlhlexer.ID not in sets:
            tmp2 = ''
            for item in tmp:
                tmp2 += str(item[1])

            try:
                print tmp2
                result = eval(tmp2)
                return result
            except:
                raise Exception('Asignment worng')

        elif zlhlexer.ID in sets:
            tmp3 = ''
            for item in tmp:
                if item[0] != zlhlexer.ID:
                    tmp3 += str(item[1])
                else:
                    tmp3 += str(self.symtab[item[1]][1])

            try:
                print tmp3
                result = eval(tmp3)
                return result
            except:
                return tmp3.replace('+','')


        


    def match(self, token_type):
        if self.cur_token[0] == token_type:
            return True
        

if __name__ == '__main__':
    prog = '''
    main{
        int a;
        float b;
        chars c;
        c = 's';
        b = 1.1;
        a = 1+1+c;
        b = 1.5;
        print c;
        print a;
        print b;
    }
    '''
    undefine = []
    lex = zlhlexer.Veclexer(prog)
    t = lex.get_next_token()

    while t[0] != zlhlexer.EOF:
        undefine.append(t)
        t = lex.get_next_token()
    #print undefine
    parser = zlhparser(undefine)
    parser.parser()
    #print parser.symtab