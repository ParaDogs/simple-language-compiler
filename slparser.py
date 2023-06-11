import sys
from lexer import Lexer, Token

class Node:
    def __repr__(self, level=0):
        pass

class NodeProgram(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self, level=0):
        res = "PROGRAM\n"
        for child in self.children:
            res += '|   ' * level
            res += "|+-"
            res += child.__repr__(level+1)
        return res

class NodeBlock(NodeProgram): pass

class NodeDeclaration(Node):
    def __init__(self, _type, id):
        self.type = _type
        self.id = id

    def __repr__(self, level=0):
        res = "DECLARATION\n"
        res += '|   ' * level
        res += "|+-"
        res += f"type: {self.type}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        return res

class NodeAssigning(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

    def __repr__(self, level=0):
        res = "ASSIGNING\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"expression: {self.expression.__repr__(level+1)}"
        return res

class NodeFunction(Node):
    def __init__(self, ret_type, id, formal_params, block):
        self.ret_type = ret_type
        self.id = id
        self.formal_params = formal_params
        self.block = block

    def __repr__(self, level=0):
        res = "FUNCTION\n"
        res += '|   ' * level
        res += "|+-"
        res += f"ret_type: {self.ret_type}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"foramal_params: {self.formal_params.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"block: {self.block.__repr__(level+1)}"
        return res

class NodeFormalParams(Node):
    def __init__(self, params):
        self.params = params
    
    def __repr__(self, level=0):
        res = "FORMAL_PARAMS\n"
        for param in self.params:
            res += '|   ' * level
            res += "|+-"
            res += param.__repr__(level+1)
        return res

class NodeIfConstruction(Node):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block
    
    def __repr__(self, level=0):
        res = "IF-CONSTRUCTION\n"
        res += '|   ' * level
        res += "|+-"
        res += f"condition: {self.condition.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"block: {self.block.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"else_block: {self.else_block.__repr__(level+1)}"
        return res
        

class NodeLiteral(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self, level=0):
        return f"{self.value}\n"

class NodeStringLiteral(NodeLiteral): pass
class NodeIntLiteral(NodeLiteral): pass
class NodeFloatLiteral(NodeLiteral): pass

class NodeVar(Node):
    def __init__(self, id):
        self.id = id
    
    def __repr__(self, level=0):
        return f"{self.id}\n"

class NodeBinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, level=0):
        c = str(self.__class__)
        pos_1 = c.find('.')+1
        pos_2 = c.find("'", pos_1)
        res = f"{c[pos_1:pos_2]}\n" # имя класса
        res += '|   ' * level
        res += "|+-"
        res += f"left : {self.left.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"right: {self.right.__repr__(level+1)}"
        return res

class NodeL(NodeBinaryOperator): pass
class NodeG(NodeBinaryOperator): pass
class NodeLE(NodeBinaryOperator): pass
class NodeGE(NodeBinaryOperator): pass
class NodeEQ(NodeBinaryOperator): pass
class NodeNEQ(NodeBinaryOperator): pass
class NodeOr(NodeBinaryOperator): pass
class NodeAnd(NodeBinaryOperator): pass

class NodePlus(NodeBinaryOperator): pass
class NodeMinus(NodeBinaryOperator): pass
class NodeDivision(NodeBinaryOperator): pass
class NodeMultiply(NodeBinaryOperator): pass
class NodeIDivision(NodeBinaryOperator): pass
class NodeMod(NodeBinaryOperator): pass


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
        params = []
        while self.token.name != Token.RBR:
            params.append(self.declaration())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeFormalParams(params)

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

    def and_operand(self) -> Node:
        if self.token.name == Token.NOT:
            self.next_token
            return NodeNot(self.and_operand())
        else:
            left = self.expression()
            op = self.token.name
            while op in {Token.L, Token.G, Token.LE, Token.GE, Token.EQ, Token.NEQ}:
                self.next_token()
                match op:
                    case Token.L:
                        left = NodeL(left, self.expression())
                    case Token.G:
                        left = NodeG(left, self.expression())
                    case Token.LE:
                        left = NodeLE(left, self.expression())
                    case Token.GE:
                        left = NodeGE(left, self.expression())
                    case Token.EQ:
                        left = NodeEQ(left, self.expression())
                    case Token.NEQ:
                        left = NodeNEQ(left, self.expression())
                op = self.token.name
            return left

    def or_operand(self) -> Node:
        left = self.and_operand()
        op = self.token.name
        while op == Token.AND:
            self.next_token()
            left = NodeAnd(left, self.and_operand())
            op = self.token.name
        return left

    def condition(self) -> Node:
        left = self.or_operand()
        op = self.token.name
        while op == Token.OR:
            self.next_token()
            left = NodeOr(left, self.or_operand())
            op = self.token.name
        return left

    def declaration(self) -> Node:
        if self.token.name == Token.ID:
            _type = self.token
            self.next_token()
            if self.token.name == Token.ID:
                id = self.token
                self.next_token()
                return NodeDeclaration(_type, id)
            else:
                self.error("Ожидался идентификатор!")
        else:
            self.error("Ожидался идентификатор типа!")

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
                            return NodeIfConstruction(condition, block, NodeBlock([]))
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
                