# Lexer Tokens

digit           :: = '0' | '1' | '2' | '3' | '4' 
                | '5' | '6' | '7' | '8' | '9'

unsigned-int-literal    ::= digit 
                        | digit unsigned-int-literal

sign            ::= '+' | '-'

INT-LITERAL     ::= sign unsigned-int-literal

FLOAT-LITERAL   ::= INT-LITERAL  '.' unsigned-int-literal

STRING-LITERAL  ::= '"' chain '"'

<!-- 
Цепочка символов. char - это все символы, кроме кавычек.
 -->
chain           ::= char | char chain

<!-- 
Идентификатор. Начинается с alpha-char - символ из латинского алфавита.
Заканчивается на последовательность id-tail
хвостовых символов alpha-digit-char - символов из латинского алфавита, вместе с цифрами и знаком '_'.
 -->
ID              ::= alpha-char | alpha-char id-tail
id-tail         ::= alpha-digit-char | alpha-digit-char id-tail

