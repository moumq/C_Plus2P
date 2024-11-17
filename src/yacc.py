import ply.yacc as yacc
from Tree import Node
from lex import tokens  # 假设词法分析部分已经定义并导出 tokens
import os

start = 'program'

# 定义语法规则
def p_program(p):
    '''program : preprocessor_directive_list declaration_list'''
    p[0] = Node('program', type=0)
    p[0].add_child(p[1])
    p[0].add_child(p[2])

def p_preprocessor_directive_list(p):
    '''preprocessor_directive_list : preprocessor_directive_list preprocessor_directive
                                   | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('preprocessor_directive_list', type=0)

def p_preprocessor_directive(p):
    '''preprocessor_directive : INCLUDE include_file
                              | IFNDEF identifier DEFINE identifier DOTS ENDIF'''
    p[0] = Node('preprocessor_directive', type=0)
    if len(p) == 3:
        p[0].add_child(Node('INCLUDE', p[1], type=1))
        p[0].add_child(Node('include_file', p[2], type=0))
    else:
        p[0].add_child(Node('IFNDEF', p[1], type=1))
        p[0].add_child(Node('identifier', p[2], type=0))
        p[0].add_child(Node('DEFINE', p[3], type=1))
        p[0].add_child(Node('identifier', p[4], type=0))
        p[0].add_child(Node('DOTS', p[5], type=1))
        p[0].add_child(Node('ENDIF', p[6], type=1))

def p_include_file(p):
    '''include_file : LT filename GT
                    | QUOTE filename QUOTE'''
    p[0] = Node('include_file', type=0)
    p[0].add_child(Node('LT', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('GT', p[3], type=1))

def p_filename(p):
    '''filename : FILENAME'''
    p[0] = Node('filename', p[1], type=1)

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = Node('identifier', p[1], type=1)

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('declaration_list', type=0)

def p_declaration(p):
    '''declaration : variable_declaration
                   | function_declaration
                   | class_declaration
                   | struct_declaration
                   | enum_declaration
                   | typedef_declaration
                   | namespace_declaration
                   | template_declaration'''
    p[0] = p[1]

def p_variable_declaration(p):
    '''variable_declaration : type identifier SEMICOLON
                            | type identifier EQUALS expression SEMICOLON'''
    p[0] = Node('variable_declaration', type=0)
    p[0].add_child(p[1])
    p[0].add_child(p[2])
    if len(p) == 4:
        p[0].add_child(Node('SEMICOLON', p[3], type=1))
    else:
        p[0].add_child(Node('EQUALS', p[3], type=1))
        p[0].add_child(p[4])
        p[0].add_child(Node('SEMICOLON', p[5], type=1))

def p_function_declaration(p):
    '''function_declaration : type identifier LPAREN parameter_list_opt RPAREN function_body_opt
                            | type identifier LPAREN parameter_list_opt RPAREN SEMICOLON'''
    p[0] = Node('function_declaration', type=0)
    p[0].add_child(p[1])
    p[0].add_child(p[2])
    p[0].add_child(Node('LPAREN', p[3], type=1))
    p[0].add_child(p[4])
    p[0].add_child(Node('RPAREN', p[5], type=1))
    if len(p) == 7:
        p[0].add_child(p[6])
    else:
        p[0].add_child(Node('SEMICOLON', p[6], type=1))

def p_class_declaration(p):
    '''class_declaration : CLASS identifier LBRACE class_member_list RBRACE'''
    p[0] = Node('class_declaration', type=0)
    p[0].add_child(Node('CLASS', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('LBRACE', p[3], type=1))
    p[0].add_child(p[4])
    p[0].add_child(Node('RBRACE', p[5], type=1))

def p_struct_declaration(p):
    '''struct_declaration : STRUCT identifier LBRACE struct_member_list RBRACE'''
    p[0] = Node('struct_declaration', type=0)
    p[0].add_child(Node('STRUCT', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('LBRACE', p[3], type=1))
    p[0].add_child(p[4])
    p[0].add_child(Node('RBRACE', p[5], type=1))

def p_enum_declaration(p):
    '''enum_declaration : ENUM identifier LBRACE enum_member_list RBRACE'''
    p[0] = Node('enum_declaration', type=0)
    p[0].add_child(Node('ENUM', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('LBRACE', p[3], type=1))
    p[0].add_child(p[4])
    p[0].add_child(Node('RBRACE', p[5], type=1))

def p_typedef_declaration(p):
    '''typedef_declaration : TYPEDEF type identifier SEMICOLON'''
    p[0] = Node('typedef_declaration', type=0)
    p[0].add_child(Node('TYPEDEF', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(p[3])
    p[0].add_child(Node('SEMICOLON', p[4], type=1))

def p_namespace_declaration(p):
    '''namespace_declaration : NAMESPACE identifier LBRACE declaration_list RBRACE'''
    p[0] = Node('namespace_declaration', type=0)
    p[0].add_child(Node('NAMESPACE', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('LBRACE', p[3], type=1))
    p[0].add_child(p[4])
    p[0].add_child(Node('RBRACE', p[5], type=1))

def p_template_declaration(p):
    '''template_declaration : TEMPLATE LT template_parameter_list GT declaration'''
    p[0] = Node('template_declaration', type=0)
    p[0].add_child(Node('TEMPLATE', p[1], type=1))
    p[0].add_child(Node('LT', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('GT', p[4], type=1))
    p[0].add_child(p[5])

def p_class_member_list(p):
    '''class_member_list : class_member_list class_member
                         | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('class_member_list', type=0)

def p_class_member(p):
    '''class_member : variable_declaration
                    | function_declaration
                    | access_specifier COLON class_member_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('access_specifier', type=0)
        p[0].add_child(p[1])
        p[0].add_child(Node('COLON', p[2], type=1))
        p[0].add_child(p[3])

def p_struct_member_list(p):
    '''struct_member_list : struct_member_list struct_member
                          | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('struct_member_list', type=0)

def p_struct_member(p):
    '''struct_member : variable_declaration
                     | function_declaration'''
    p[0] = p[1]

def p_enum_member_list(p):
    '''enum_member_list : enum_member_list COMMA enum_member
                        | enum_member'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].add_child(Node('COMMA', p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('enum_member_list', type=0)
        p[0].add_child(p[1])

def p_enum_member(p):
    '''enum_member : identifier
                   | identifier EQUALS integer_literal'''
    if len(p) == 2:
        p[0] = Node('enum_member', type=0)
        p[0].add_child(p[1])
    else:
        p[0] = Node('enum_member', type=0)
        p[0].add_child(p[1])
        p[0].add_child(Node('EQUALS', p[2], type=1))
        p[0].add_child(p[3])

def p_access_specifier(p):
    '''access_specifier : PUBLIC
                        | PRIVATE
                        | PROTECTED'''
    p[0] = Node('access_specifier', p[1], type=1)

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL
            | VOID
            | class_type
            | pointer_type
            | reference_type
            | array_type
            | template_type'''
    p[0] = p[1]

def p_class_type(p):
    '''class_type : identifier'''
    p[0] = p[1]

def p_pointer_type(p):
    '''pointer_type : type TIMES'''
    p[0] = Node('pointer_type', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('TIMES', p[2], type=1))

def p_reference_type(p):
    '''reference_type : type AMPERSAND'''
    p[0] = Node('reference_type', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('AMPERSAND', p[2], type=1))

def p_array_type(p):
    '''array_type : type LBRACKET integer_literal RBRACKET'''
    p[0] = Node('array_type', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('LBRACKET', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('RBRACKET', p[4], type=1))

def p_template_type(p):
    '''template_type : identifier LT type_list GT'''
    p[0] = Node('template_type', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('LT', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('GT', p[4], type=1))

def p_type_list(p):
    '''type_list : type_list COMMA type
                 | type'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].add_child(Node('COMMA', p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('type_list', type=0)
        p[0].add_child(p[1])

def p_parameter_list_opt(p):
    '''parameter_list_opt : parameter_list
                          | empty'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].add_child(Node('COMMA', p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('parameter_list', type=0)
        p[0].add_child(p[1])

def p_parameter(p):
    '''parameter : type identifier'''
    p[0] = Node('parameter', type=0)
    p[0].add_child(p[1])
    p[0].add_child(p[2])

def p_template_parameter_list(p):
    '''template_parameter_list : template_parameter_list COMMA template_parameter
                               | template_parameter'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].add_child(Node('COMMA', p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('template_parameter_list', type=0)
        p[0].add_child(p[1])

def p_template_parameter(p):
    '''template_parameter : TYPENAME identifier
                          | CLASS identifier'''
    p[0] = Node('template_parameter', type=0)
    p[0].add_child(Node(p[1], p[1], type=1))
    p[0].add_child(p[2])

def p_function_body_opt(p):
    '''function_body_opt : function_body
                         | empty'''
    p[0] = p[1]

def p_function_body(p):
    '''function_body : LBRACE statement_list RBRACE'''
    p[0] = Node('function_body', type=0)
    p[0].add_child(Node('LBRACE', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('RBRACE', p[3], type=1))

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('statement_list', type=0)

def p_statement(p):
    '''statement : expression_statement
                 | if_statement
                 | for_statement
                 | while_statement
                 | do_while_statement
                 | return_statement
                 | compound_statement
                 | switch_statement
                 | break_statement
                 | continue_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = Node('expression_statement', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('SEMICOLON', p[2], type=1))

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement else_opt'''
    p[0] = Node('if_statement', type=0)
    p[0].add_child(Node('IF', p[1], type=1))
    p[0].add_child(Node('LPAREN', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('RPAREN', p[4], type=1))
    p[0].add_child(p[5])
    p[0].add_child(p[6])

def p_else_opt(p):
    '''else_opt : ELSE statement
                | empty'''
    if len(p) == 3:
        p[0] = Node('else_opt', type=0)
        p[0].add_child(Node('ELSE', p[1], type=1))
        p[0].add_child(p[2])
    else:
        p[0] = Node('else_opt', type=0)

def p_for_statement(p):
    '''for_statement : FOR LPAREN expression_statement_opt expression_opt SEMICOLON expression_opt RPAREN statement'''
    p[0] = Node('for_statement', type=0)
    p[0].add_child(Node('FOR', p[1], type=1))
    p[0].add_child(Node('LPAREN', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(p[4])
    p[0].add_child(Node('SEMICOLON', p[5], type=1))
    p[0].add_child(p[6])
    p[0].add_child(Node('RPAREN', p[7], type=1))
    p[0].add_child(p[8])

def p_expression_statement_opt(p):
    '''expression_statement_opt : expression_statement
                                | empty'''
    p[0] = p[1]

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    p[0] = p[1]

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = Node('while_statement', type=0)
    p[0].add_child(Node('WHILE', p[1], type=1))
    p[0].add_child(Node('LPAREN', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('RPAREN', p[4], type=1))
    p[0].add_child(p[5])

def p_do_while_statement(p):
    '''do_while_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON'''
    p[0] = Node('do_while_statement', type=0)
    p[0].add_child(Node('DO', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('WHILE', p[3], type=1))
    p[0].add_child(Node('LPAREN', p[4], type=1))
    p[0].add_child(p[5])
    p[0].add_child(Node('RPAREN', p[6], type=1))
    p[0].add_child(Node('SEMICOLON', p[7], type=1))

def p_return_statement(p):
    '''return_statement : RETURN expression_opt SEMICOLON'''
    p[0] = Node('return_statement', type=0)
    p[0].add_child(Node('RETURN', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('SEMICOLON', p[3], type=1))

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE'''
    p[0] = Node('compound_statement', type=0)
    p[0].add_child(Node('LBRACE', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('RBRACE', p[3], type=1))

def p_switch_statement(p):
    '''switch_statement : SWITCH LPAREN expression RPAREN LBRACE switch_case_list default_case_opt RBRACE'''
    p[0] = Node('switch_statement', type=0)
    p[0].add_child(Node('SWITCH', p[1], type=1))
    p[0].add_child(Node('LPAREN', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('RPAREN', p[4], type=1))
    p[0].add_child(Node('LBRACE', p[5], type=1))
    p[0].add_child(p[6])
    p[0].add_child(p[7])
    p[0].add_child(Node('RBRACE', p[8], type=1))

def p_switch_case_list(p):
    '''switch_case_list : switch_case_list switch_case
                        | empty'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].add_child(p[2])
    else:
        p[0] = Node('switch_case_list', type=0)

def p_switch_case(p):
    '''switch_case : CASE literal COLON statement_list'''
    p[0] = Node('switch_case', type=0)
    p[0].add_child(Node('CASE', p[1], type=1))
    p[0].add_child(p[2])
    p[0].add_child(Node('COLON', p[3], type=1))
    p[0].add_child(p[4])

def p_default_case_opt(p):
    '''default_case_opt : default_case
                        | empty'''
    p[0] = p[1]

def p_default_case(p):
    '''default_case : DEFAULT COLON statement_list'''
    p[0] = Node('default_case', type=0)
    p[0].add_child(Node('DEFAULT', p[1], type=1))
    p[0].add_child(Node('COLON', p[2], type=1))
    p[0].add_child(p[3])

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON'''
    p[0] = Node('break_statement', type=0)
    p[0].add_child(Node('BREAK', p[1], type=1))
    p[0].add_child(Node('SEMICOLON', p[2], type=1))

def p_continue_statement(p):
    '''continue_statement : CONTINUE SEMICOLON'''
    p[0] = Node('continue_statement', type=0)
    p[0].add_child(Node('CONTINUE', p[1], type=1))
    p[0].add_child(Node('SEMICOLON', p[2], type=1))

def p_expression(p):
    '''expression : primary_expression
                  | expression operator expression
                  | unary_operator expression
                  | expression postfix_operator'''
    if len(p) == 2:
        p[0] = Node('expression', type=0)
        p[0].add_child(p[1])
    elif len(p) == 4:
        p[0] = Node('expression', type=0)
        p[0].add_child(p[1])
        p[0].add_child(Node(p[2], p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('expression', type=0)
        p[0].add_child(Node(p[1], p[1], type=1))
        p[0].add_child(p[2])

def p_primary_expression(p):
    '''primary_expression : identifier
                          | literal
                          | LPAREN expression RPAREN
                          | function_call
                          | member_access
                          | pointer_access'''
    if len(p) == 2:
        p[0] = Node('primary_expression', type=0)
        p[0].add_child(p[1])
    elif len(p) == 4:
        p[0] = Node('primary_expression', type=0)
        p[0].add_child(Node('LPAREN', p[1], type=1))
        p[0].add_child(p[2])
        p[0].add_child(Node('RPAREN', p[3], type=1))
    else:
        p[0] = Node('primary_expression', type=0)
        p[0].add_child(p[1])

def p_function_call(p):
    '''function_call : identifier LPAREN argument_list_opt RPAREN'''
    p[0] = Node('function_call', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('LPAREN', p[2], type=1))
    p[0].add_child(p[3])
    p[0].add_child(Node('RPAREN', p[4], type=1))

def p_member_access(p):
    '''member_access : primary_expression DOT identifier'''
    p[0] = Node('member_access', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('DOT', p[2], type=1))
    p[0].add_child(p[3])

def p_pointer_access(p):
    '''pointer_access : primary_expression ARROW identifier'''
    p[0] = Node('pointer_access', type=0)
    p[0].add_child(p[1])
    p[0].add_child(Node('ARROW', p[2], type=1))
    p[0].add_child(p[3])

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                         | empty'''
    p[0] = p[1]

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = Node('argument_list', type=0)
        p[0].add_child(p[1])
        p[0].add_child(Node('COMMA', p[2], type=1))
        p[0].add_child(p[3])
    else:
        p[0] = Node('argument_list', type=0)
        p[0].add_child(p[1])

def p_unary_operator(p):
    '''unary_operator : MINUS
                      | NOT
                      | PLUSPLUS
                      | MINUSMINUS'''
    p[0] = Node('unary_operator', p[1], type=1)

def p_postfix_operator(p):
    '''postfix_operator : PLUSPLUS
                        | MINUSMINUS'''
    p[0] = Node('postfix_operator', p[1], type=1)

def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | MOD
                | EQEQ
                | NOTEQ
                | LT
                | GT
                | LE
                | GE
                | ANDAND
                | OROR
                | EQUALS
                | PLUSEQ
                | MINUSEQ
                | TIMESEQ
                | DIVIDEEQ
                | MODEQ'''
    p[0] = Node('operator', p[1], type=1)

def p_literal(p):
    '''literal : integer_literal
               | float_literal
               | boolean_literal
               | string_literal'''
    p[0] = Node('literal', type=0)
    p[0].add_child(p[1])

def p_integer_literal(p):
    '''integer_literal : INTEGER'''
    p[0] = Node('integer_literal', p[1], type=1)

def p_float_literal(p):
    '''float_literal : FLOAT'''
    p[0] = Node('float_literal', p[1], type=1)

def p_boolean_literal(p):
    '''boolean_literal : TRUE
                       | FALSE
                       | ZERO
                       | ONE'''
    p[0] = Node('boolean_literal', p[1], type=1)

def p_string_literal(p):
    '''string_literal : STRING'''
    p[0] = Node('string_literal', p[1], type=1)

def p_empty(p):
    '''empty :'''
    p[0] = None

# 错误处理
def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()
def main():
    import os

    file_path = input("请输入C++文件的路径: ")

    if not os.path.isfile(file_path):
        print(f"文件未找到: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    result = parser.parse(data)
    if result:
        print(result.to_json())
    else:
        print("解析失败。")

if __name__ == "__main__":
    main()