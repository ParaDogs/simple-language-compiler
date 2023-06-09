from lexer import Lexer, Token
from slparser import Parser

f = open(r"C:/Users/nervo/OneDrive/Рабочий стол/compiler/example.sl", 'r')

pars = Parser(Lexer(f))


# t = lex.get_next_token()
# while t.name != Token.EOF:
#     print(t)
#     t = lex.get_next_token()
# print(t)
# f.close()

print(pars.parse())