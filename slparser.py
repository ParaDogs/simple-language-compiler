import sys
from lexer import Lexer, Token

class Node:
    def __repr__(self, level=0):
        pass

    def get_class_name(self):
        c = str(self.__class__)
        pos_1 = c.find('.')+1
        pos_2 = c.find("'", pos_1)
        return f"{c[pos_1:pos_2]}"

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
        res += f"type: {self.type.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        return res

class NodeAssigning(Node):
    def __init__(self, var, expression):
        self.var = var
        self.expression = expression

    def __repr__(self, level=0):
        res = "ASSIGNING\n"
        res += '|   ' * level
        res += "|+-"
        res += f"left-side : {self.var.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"right-side: {self.expression.__repr__(level+1)}"
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
        res += f"ret_type: {self.ret_type.__repr__(level+1)}"
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

class NodeSequence(Node):
    def __init__(self, members):
        self.members = members
    
    def __repr__(self, level=0):
        res = f"SEQUENCE\n"
        for param in self.members:
            res += '|   ' * level
            res += "|+-"
            res += param.__repr__(level+1)
        return res

class NodeParams(Node):
    def __init__(self, params):
        self.params = params
    
    def __repr__(self, level=0):
        res = f"{self.get_class_name()}\n"
        for param in self.params:
            res += '|   ' * level
            res += "|+-"
            res += param.__repr__(level+1)
        return res

class NodeFormalParams(NodeParams): pass
class NodeActualParams(NodeParams): pass

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
        
class NodeWhileConstruction(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self, level=0):
        res = "WHILE-CONSTRUCTION\n"
        res += '|   ' * level
        res += "|+-"
        res += f"condition: {self.condition.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"block: {self.block.__repr__(level+1)}"
        return res

class NodeReturnStatement(Node):
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self, level=0):
        res = "RETURN-STATEMETS\n"
        res += '|   ' * level
        res += "|+-"
        res += f"expression: {self.expression.__repr__(level+1)}"
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
        res = f"{self.get_class_name()}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        return res

class NodeAtomType(Node):
    def __init__(self, id):
        self.id = id

    def __repr__(self, level=0):
        res = f"ATOM-TYPE\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        return res

class NodeComplexType(Node):
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __repr__(self, level=0):
        res = f"COMPLEX-TYPE\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"size: {self.size}\n"
        return res

class NodeFunctionCall(Node):
    def __init__(self, id, actual_params):
        self.id = id
        self.actual_params = actual_params

    def __repr__(self, level=0):
        res = f"FUNCTION-CALL\n"
        res += '|   ' * level
        res += "|+-"
        res += f"id: {self.id}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"actual_params: {self.actual_params.__repr__(level+1)}"
        return res
        
class NodeIndexAccess(Node):
    def __init__(self, var, index):
        self.var = var
        self.index = index

    def __repr__(self, level=0):
        res = f"INDEX-ACCESS\n"
        res += '|   ' * level
        res += "|+-"
        res += f"var: {self.var.__repr__(level+1)}"
        res += '|   ' * level
        res += "|+-"
        res += f"index: {self.index.__repr__(level+1)}"
        return res
        
class NodeUnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand
    
    def __repr__(self, level=0):
        res = f"{self.get_class_name()}\n"
        res += '|   ' * level
        res += "|+-"
        res += f"operand : {self.operand.__repr__(level+1)}"
        return res

class NodeUnaryMinus(NodeUnaryOperator): pass
class NodeNot(NodeUnaryOperator): pass

class NodeBinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, level=0):
        res = f"{self.get_class_name()}\n"
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
        params = []
        while self.token.name != Token.RBR:
            params.append(self.expression())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeActualParams(params)

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
                    return NodeIndexAccess(NodeVar(first_token), index)
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

    def logical_operand(self) -> Node:
        if self.token.name == Token.NOT:
            self.next_token()
            return NodeNot(self.logical_operand())
        elif self.token.name == Token.LBR:
            self.next_token()
            condition = self.condition()
            if self.token.name == Token.RBR:
                self.next_token()
                return condition
            else:
                self.error("Ожидалась закрывающая скобка ')'!")
        else:
            return self.expression()

    def and_operand(self) -> Node:
        left = self.logical_operand()
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

    def type(self) -> Node:
        id = self.token
        self.next_token()
        if self.token.name == Token.LSBR:
            self.next_token()
            if self.token.name == Token.INT_LITERAL:
                size = self.token
                self.next_token()
                if self.token.name == Token.RSBR:
                    self.next_token()
                    return NodeComplexType(id, size)
                else:
                    self.error("Ожидалась ']' при указании размера массива!")
            else:
                self.error("Ожидался целочисленый литерал при указании размера массива!")
        else:
            return NodeAtomType(id)

    def sequence(self) -> Node:
        members = []
        while self.token.name != Token.RSBR:
            members.append(self.expression())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeSequence(members)

    def declaration(self) -> Node:
        if self.token.name == Token.ID:
            _type = self.type()
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
                # например int abc 
                if self.token.name == Token.ID:
                    name = self.token
                    self.next_token()
                    return NodeDeclaration(NodeAtomType(first_token), name)
                # например int[10] abc
                elif self.token.name == Token.LSBR:
                    self.next_token()
                    if self.token.name == Token.INT_LITERAL:
                        size = self.token
                        self.next_token()
                        if self.token.name == Token.RSBR:
                            self.next_token()
                            if self.token.name == Token.ID:
                                name = self.token
                                self.next_token()
                                return NodeDeclaration(NodeComplexType(first_token, size), name)
                            else:
                                self.error("Ожидался идентификатор переменной!")
                        else:
                            self.error("Ожидалась ']' при указании размера массива!")
                    else:
                        self.error("Ожидался целочисленый литерал при указании размера массива!")
                # например abc = 123 или abc = [1,2,3]
                elif self.token.name == Token.ASSIGN:
                    self.next_token()
                    if self.token.name == Token.LSBR:
                        self.next_token()
                        sequence = self.sequence()
                        if self.token.name == Token.RSBR:
                            self.next_token()
                            return NodeAssigning(NodeVar(first_token), sequence)
                        else:
                            self.error("Ожидалась закрывающая скобка ']' при записи последовательности!")
                    else:
                        return NodeAssigning(NodeVar(first_token), self.expression())
                # например abc(1,3,4)
                elif self.token.name == Token.LBR:
                    self.next_token()
                    actual_params = self.actual_params()
                    if self.token.name == Token.RBR:
                        self.next_token()
                        return NodeFunctionCall(first_token, actual_params)
                else:
                    self.error("Ожидалось объявление переменной, присваивание или вызов функции!")

            # function
            case Token.FUNCTION:
                # пропускаем токен FUNCTION
                self.next_token()
                # следующий токен содержит тип возвр. значения. это ID типа.
                if self.token.name == Token.ID:
                    # сохраним тип
                    first_token = self.type()
                    # следующий токен содержит ID функции
                    if self.token.name == Token.ID:
                        # сохраним имя функции
                        name = self.token
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
                                        return NodeFunction(first_token, name, formal_params, block)
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
                