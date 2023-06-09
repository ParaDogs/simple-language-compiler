import sys
from lexer import Lexer, Token

class Node: pass

class NodeProgram(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        s = '\n'.join([str(x) for x in self.children])
        return s

class NodeBlock(NodeProgram): pass

class NodeDeclaration(Node):
    def __init__(self, _type, id):
        self.type = _type
        self.id = id

    def __repr__(self):
        return f"DECLARATION <{self.type}, {self.id}>"

class NodeAssigning(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

    def __repr__(self):
        return f"ASSIGNING <{self.id}, {self.expression}>"

class NodeFunction(Node):
    def __init__(self, ret_type, id, formal_params, block):
        self.ret_type = ret_type
        self.id = id
        self.formal_params = formal_params
        self.block = block

    def __repr__(self):
        return f"FUNCTION <{self.ret_type}, {self.id}, {self.formal_params}, <{self.block}>>"

class NodeLiteral(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"

class NodeStringLiteral(NodeLiteral): pass
class NodeIntLiteral(NodeLiteral): pass
class NodeFloatLiteral(NodeLiteral): pass

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = self.lexer.get_next_token()

    def next_token(self):
        self.token = self.lexer.get_next_token()

    def error(self, msg):
        print(f'Ошибка синтаксического анализа ({self.lexer.lineno}, {self.lexer.pos}): {msg}')
        sys.exit(1)

    def block(self) -> Node:
        statements = []
        while self.token.name != Token.RCBR:
            statements.append(self.statement())
            if self.token.name == Token.SEMI:
                self.next_token()
            else:
                 self.error("Ожидалась ';'!")
        return NodeBlock(statements)

    def actual_params(self) -> Node:
        pass

    def formal_params(self) -> Node:
        declaration = self.de

    def operand(self) -> Node:
        first_token = self.token
        if self.token.name == Token.STRING_LITERAL:
            self.next_token()
            return NodeStringLiteral(first_token)
        elif self.token.name == Token.INT_LITERAL:
            self.next_token()
            return NodeIntLiteral(first_token)
        elif self.token.name == Token.FLOAT_LITERAL:
            self.next_token()
            return NodeFloatLiteral(first_token)
        elif self.token.name == Token.ID:
            self.next_token()
            if self.token.name == Token.LBR:
                self.next_token()
                if self.token.name == Token.RBR:
                    self.next_token()
                    return NodeFunctionCall(first_token, [])
                else:
                    actual_params = self.actual_params()
                    if self.token.name == Token.RBR:
                        self.next_token()
                        return NodeFunctionCall(first_token, actual_params)
                    else:
                        self.error("Ожидалась закрывающая скобка ')'!")
            elif self.token.name == Token.LSBR:
                self.next_token()
                index = self.expression()
                if self.token.name == Token.RSBR:
                    self.next_token()
                    return NodeIndexAccess(first_token, index)
                else:
                    self.error("Ожидалась закрывающая скобка ']'!")
            else:
                return NodeVar(first_token)
        elif self.token.name == Token.LBR:
            self.next_token()
            expression = self.expression()
            if self.token.name == Token.RBR:
                self.next_token()
                return expression
            else:
                self.error("Ожидалась закрывающая скобка ')'!")


    def factor(self) -> Node:
        if self.token.name == Token.MINUS:
            self.next_token()
            return NodeUnaryMinus(self.operand())
        else:
            return self.operand()

    def term(self) -> Node:
        left = self.factor()
        op = self.token.name
        while op in {Token.ASTERISK, Token.SLASH, Token.DSLASH, Token.PERCENT}:
            self.next_token()
            match op:
                case Token.ASTERISK:
                    left = NodeMultiply(left, self.factor())
                case Token.SLASH:
                    left = NodeDivision(left, self.factor())
                case Token.DSLASH:
                    left = NodeIDivision(left, self.factor())
                case Token.PERCENT:
                    left = NodeMod(left, self.factor())
            op = self.token.name
        return left

    def expression(self) -> Node:
        left = self.term()
        op = self.token.name
        while op in {Token.PLUS, Token.MINUS}:
            self.next_token()
            match op:
                case Token.PLUS:
                    left = NodePlus(left, self.term())
                case Token.MINUS:
                    left = NodeMinus(left, self.term())
            op = self.token.name
        return left

    def statement(self) -> Node:
        match self.token.name:
            # declaration | assigning | function-call
            case Token.ID:
                first_token = self.token
                self.next_token()
                if self.token.name == Token.ID:
                    second_token = self.token
                    self.next_token()
                    return NodeDeclaration(first_token, second_token)
                elif self.token.name == Token.ASSIGN:
                    self.next_token()
                    return NodeAssigning(first_token, self.expression())
                elif self.token.name == Token.LBR:
                    self.next_token()
                    if self.token.name == Token.RBR:
                        return NodeFunctionCall(first_token, [])
                    else:
                        return NodeFunctionCall(first_token, self.actual_params())
                else:
                    self.error("Ожидалось объявление переменной, присваивание или вызов функции!")

            # function ...
            case Token.FUNCTION:
                # пропускаем токен FUNCTION
                self.next_token()
                # следующий токен содержит тип возвр. значения. это ID типа.
                if self.token.name == Token.ID:
                    # сохраним тип в первый токен
                    first_token = self.token
                    # возмем следующий токен
                    self.next_token()
                    # следующий токен содержит ID функции
                    if self.token.name == Token.ID:
                        # сохраним имя функции во второй токен
                        second_token = self.token
                        # смотрим на следующий токен
                        self.next_token()
                        # следующий токен ( - скобка перед формальными параметрами
                        if self.token.name == Token.LBR:
                            # пропускаем скобку
                            self.next_token()
                            # случай функции без параметров
                            if self.token.name == Token.RBR:
                                formal_params = []
                            else:
                                # начинаем разбор формальных параметров
                                formal_params = self.formal_params()
                            # после разбора формальных параметров лексер должен смотреть на закрывающую скобку )
                            if self.token.name == Token.RBR:
                                # пропускаем скобку
                                self.next_token()
                                #следующий токен { - скобка перед телом функции
                                if self.token.name == Token.LCBR:
                                    # пропускаем скобку
                                    self.next_token()
                                    # начинаем разбирать тело
                                    block = self.block()
                                    # после разбора тела функции мы должны встретить закрывающую скобку }
                                    if self.token.name == Token.RCBR:
                                        self.next_token()
                                        return NodeFunction(first_token, second_token, formal_params, block)
                                    else:
                                        self.error("Ожидалась закрывающая фигурная скобка!")
                                else:
                                    self.error("Ожидалась открывающая скобка '{' и тело функции!")
                            else:
                                self.error("Ожидалась закрывающая скобка ')'!")
                        else:
                            self.error("Ожидалась открывающая скобка '(' и параметры функции!")
                    else:
                        self.error("Ожидалось указание типа возвращаемого значения функции!")

            case Token.IF:
                self.next_token()
                condition = self.condition()
                if self.token.name == Token.LCBR:
                    self.next_token()
                    block = self.block()
                    if self.token.name == Token.RCBR:
                        self.next_token()
                        if self.token.name == Token.ELSE:
                            self.next_token()
                            if self.token.name == Token.LCBR:
                                self.next_token()
                                else_block = self.block()
                                if self.token.name == Token.RCBR:
                                    self.next_token()
                                    return NodeIfConstruction(condition, block, else_block)
                                else:
                                    self.error("Ожидалась закрывающая скобка '}' для блока else!")
                            else:
                                self.error("Ожидалась открывающая скобка '{' для блока else!")
                        else:
                            # возврат условной конструкции без блока else
                            return NodeIfConstruction(condition, block, [])
                    else:
                        self.error("Ожидалась закрывающая скобка '}' для блока if!")
                else:
                    self.error("Ожидалась открывающая скобка '{' для блока if!")

            case Token.WHILE:
                self.next_token()
                condition = self.condition()
                if self.token.name == Token.LCBR:
                    self.next_token()
                    block = self.block()
                    if self.token.name == Token.RCBR:
                        self.next_token()
                        return NodeWhileConstruction(condition, block)
                    else:
                        self.error("Ожидалась закрывающая скобка '}' для блока while!")
                else:
                    self.error("Ожидалась открывающая скобка '{' для блока while!")

            case Token.RETURN:
                self.next_token()
                expression = self.expression()
                return NodeReturnStatement(expression)


    def parse(self) -> Node:
        '''
        program ::= statement SEMI EOF 
                |   statement SEMI program
        '''
        if self.token.name == Token.EOF:
            self.error("Пустой файл!")
        else:
            statements = []
            while self.token.name != Token.EOF:
                statements.append(self.statement())
                if self.token.name == Token.SEMI:
                    self.next_token()
                else:
                    self.error("Ожидалась ';'!")
            return NodeProgram(statements)
                