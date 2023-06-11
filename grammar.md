# Simple Language

## Program
<!--
Программа - это последовательность инструкций,
оканчивающаяся концом файла EOF.
После каждой инструкции стоит ';'
 -->
program         ::= statement SEMI EOF 
                |   statement SEMI program

## Literals
<!-- 
Это подмножество токенов лексера, они описаны в tokens.md
 -->
literal         ::= STRING-LITERAL 
                | INT-LITERAL
                | FLOAT-LITERAL
<!-- 
Кроме них в tokens.md описаны и прочие токены лексера.
В этом файле они записаны капсом.
 -->

## Type
<!-- 
Тип переменной может быть "атомарным" и "сложным".
 -->
type            ::= atom-type
                | complex-type

<!-- 
"Атомарные" типы приведены ниже.
К переменным такого типа не может применяться
операция обращения по индексу.
 -->
atom-type       ::= 'bool'
                |   'int'
                |   'float'
                |   'string'

<!-- 
"Сложные" типы служат для создания массивов и
образуются из "атомарных" как показано ниже.
 -->
complex-type    ::= type LSBR INT-LITERAL RSBR

## Condition
<!--
Грамматика условий отражает приоритет операций.
1. арифметические
2. сравнения (> < == ...)
3. not
4. and
5. or
 -->
condition       ::= or-operand OR condition 
                | or-operand  

or-operand      ::= and-operand AND or-operand
                | and-operand

and-operand     ::= logical-operand compare-operator and-operand
                | logical-operand

logical-operand ::= expression
                | NOT logical-operand
                | LBR condition RBR


compare-operator ::= L | G | LE | GE | EQ | NEQ

## Expression
<!-- 
Грамматика выражений отражает приоритет
арифметических операций.
1. Скобки
2. Унарный минус
3. Умножение, деление, остаток
4. Сложение, вычитание
 -->
expression      ::= term PLUS expression
                | term MINUS expression
                | term

term            ::= factor ASTERISK term
                | factor SLASH term
                | factor DSLASH term
                | factor PERCENT term
                | factor

factor          ::= operand
                | MINUS operand

operand         ::= literal 
                | ID
                | function-call
                | index-access
                | LBR expression RBR

function-call   ::= ID LBR actual-params RBR
                | ID LBR RBR

index-access    ::= ID LSBR expression RSBR

## Params
<!-- 
Параметры при объявлении функции и при её вызове
соответственно делятся на формальные и фактические.
Формальные параметры - это последовательность объявлений
переменных, а фактические - это последовательность
выражений.
 -->
formal-params   ::= declaration 
                | declaration COMMA formal-params

actual-params   ::= expression
                | expression COMMA actual-params

## Statement
<!-- 
Инструкцией может быть:
объявление переменной, присваивание значения переменной,
объявление функции, ветвление, цикл.
 -->
statement       ::= declaration 
                | assigning
                | function-call
                | function-construction 
                | if-construction  
                | while-construction
                | return-statement

return-statement    ::= RETURN expression 

### Declaration
<!-- 
Для объявления переменной 
указывается её тип и идентификатор.
 -->
declaration     ::= type ID

### Assigning
<!-- 
Переменной присваивается значение некоторого выражения.
 -->
assigning       ::= ID ASSIGN expression
                | ID ASSIGN LSBR sequence RSBR
                | ID ASSIGN LSBR RSBR

sequence        ::= expression
                | expression COMMA sequence

### FUNCTION-construction
<!-- 
Функция объявляется с использованием ключевого слова
'function', указанием типа возвращаемого значения,
формальных параметров, её идентификатора и тела.
 -->
function-construction   ::= FUNCTION type ID LBR formal-params RBR LCBR block RCBR
                        | FUNCTION type ID LBR RBR LCBR block RCBR

### IF-construction

if-construction ::= IF condition LCBR block RCBR
                | IF condition LCBR block RCBR 'else' LCBR block RCBR 

### WHILE-construction

while-construction ::= WHILE condition LCBR block RCBR

## Block

block           ::= statement SEMI 
                | statement SEMI block 
                