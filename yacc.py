import ply.yacc as yacc
from lex import tokens  # 假设词法分析部分已经定义并导出 tokens

# 定义语法规则
def p_program(p):
    '''program : preprocessor_directive_list declaration_list'''
    p[0] = ('program', p[1], p[2])

def p_preprocessor_directive_list(p):
    '''preprocessor_directive_list : preprocessor_directive_list preprocessor_directive
                                   | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_preprocessor_directive(p):
    '''preprocessor_directive : INCLUDE include_file
                              | IFNDEF identifier DEFINE identifier DOTS ENDIF'''
    if len(p) == 3:
        p[0] = ('include', p[2])
    else:
        p[0] = ('ifndef', p[2], p[4])

def p_include_file(p):
    '''include_file : LT filename GT
                    | QUOTE filename QUOTE'''
    p[0] = p[2]

def p_filename(p):
    '''filename : IDENTIFIER'''
    p[0] = p[1]

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = p[1]

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

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
    if len(p) == 4:
        p[0] = ('var_decl', p[1], p[2])
    else:
        p[0] = ('var_decl', p[1], p[2], p[4])

def p_function_declaration(p):
    '''function_declaration : type identifier LPAREN parameter_list_opt RPAREN function_body_opt
                            | type identifier LPAREN parameter_list_opt RPAREN SEMICOLON'''
    if len(p) == 6:
        p[0] = ('func_decl', p[1], p[2], p[4])
    else:
        p[0] = ('func_decl', p[1], p[2], p[4], p[6])

def p_class_declaration(p):
    '''class_declaration : CLASS identifier LBRACE class_member_list RBRACE'''
    p[0] = ('class_decl', p[2], p[4])

def p_struct_declaration(p):
    '''struct_declaration : STRUCT identifier LBRACE struct_member_list RBRACE'''
    p[0] = ('struct_decl', p[2], p[4])

def p_enum_declaration(p):
    '''enum_declaration : ENUM identifier LBRACE enum_member_list RBRACE'''
    p[0] = ('enum_decl', p[2], p[4])

def p_typedef_declaration(p):
    '''typedef_declaration : TYPEDEF type identifier SEMICOLON'''
    p[0] = ('typedef_decl', p[2], p[3])

def p_namespace_declaration(p):
    '''namespace_declaration : NAMESPACE identifier LBRACE declaration_list RBRACE'''
    p[0] = ('namespace_decl', p[2], p[4])

def p_template_declaration(p):
    '''template_declaration : TEMPLATE LT template_parameter_list GT declaration'''
    p[0] = ('template_decl', p[3], p[5])

def p_class_member_list(p):
    '''class_member_list : class_member_list class_member
                         | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : variable_declaration
                    | function_declaration
                    | access_specifier COLON class_member_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('access_spec', p[1], p[3])

def p_struct_member_list(p):
    '''struct_member_list : struct_member_list struct_member
                          | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_struct_member(p):
    '''struct_member : variable_declaration
                     | function_declaration'''
    p[0] = p[1]

def p_enum_member_list(p):
    '''enum_member_list : enum_member_list COMMA enum_member
                        | enum_member'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_enum_member(p):
    '''enum_member : identifier
                   | identifier EQUALS integer_literal'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])

def p_access_specifier(p):
    '''access_specifier : PUBLIC
                        | PRIVATE
                        | PROTECTED'''
    p[0] = p[1]

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
    p[0] = ('pointer', p[1])

def p_reference_type(p):
    '''reference_type : type AMPERSAND'''
    p[0] = ('reference', p[1])

def p_array_type(p):
    '''array_type : type LBRACKET integer_literal RBRACKET'''
    p[0] = ('array', p[1], p[3])

def p_template_type(p):
    '''template_type : identifier LT type_list GT'''
    p[0] = ('template', p[1], p[3])

def p_type_list(p):
    '''type_list : type_list COMMA type
                 | type'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parameter_list_opt(p):
    '''parameter_list_opt : parameter_list
                          | empty'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parameter(p):
    '''parameter : type identifier'''
    p[0] = (p[1], p[2])

def p_template_parameter_list(p):
    '''template_parameter_list : template_parameter_list COMMA template_parameter
                               | template_parameter'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_template_parameter(p):
    '''template_parameter : TYPENAME identifier
                          | CLASS identifier'''
    p[0] = (p[1], p[2])

def p_function_body_opt(p):
    '''function_body_opt : function_body
                         | empty'''
    p[0] = p[1]

def p_function_body(p):
    '''function_body : LBRACE statement_list RBRACE'''
    p[0] = p[2]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

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
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement else_opt'''
    p[0] = ('if', p[3], p[5], p[6])

def p_else_opt(p):
    '''else_opt : ELSE statement
                | empty'''
    p[0] = p[1]

def p_for_statement(p):
    '''for_statement : FOR LPAREN expression_statement_opt expression_opt SEMICOLON expression_opt RPAREN statement'''
    p[0] = ('for', p[3], p[4], p[6], p[8])

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
    p[0] = ('while', p[3], p[5])

def p_do_while_statement(p):
    '''do_while_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('do_while', p[2], p[5])

def p_return_statement(p):
    '''return_statement : RETURN expression_opt SEMICOLON'''
    p[0] = ('return', p[2])

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE'''
    p[0] = p[2]

def p_switch_statement(p):
    '''switch_statement : SWITCH LPAREN expression RPAREN LBRACE switch_case_list RBRACE'''
    p[0] = ('switch', p[3], p[6])

def p_switch_case_list(p):
    '''switch_case_list : switch_case_list switch_case
                        | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_switch_case(p):
    '''switch_case : CASE integer_literal COLON statement_list
                   | DEFAULT COLON statement_list'''
    if len(p) == 5:
        p[0] = ('case', p[2], p[4])
    else:
        p[0] = ('default', p[3])

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON'''
    p[0] = ('break',)

def p_continue_statement(p):
    '''continue_statement : CONTINUE SEMICOLON'''
    p[0] = ('continue',)

def p_expression(p):
    '''expression : primary_expression
                  | expression operator expression
                  | unary_operator expression
                  | expression postfix_operator'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1], p[2])

def p_primary_expression(p):
    '''primary_expression : identifier
                          | literal
                          | LPAREN expression RPAREN
                          | function_call
                          | member_access
                          | pointer_access'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_function_call(p):
    '''function_call : identifier LPAREN argument_list_opt RPAREN'''
    p[0] = ('func_call', p[1], p[3])

def p_member_access(p):
    '''member_access : primary_expression DOT identifier'''
    p[0] = ('member_access', p[1], p[3])

def p_pointer_access(p):
    '''pointer_access : primary_expression ARROW identifier'''
    p[0] = ('pointer_access', p[1], p[3])

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                         | empty'''
    p[0] = p[1]

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_unary_operator(p):
    '''unary_operator : MINUS
                      | NOT
                      | PLUSPLUS
                      | MINUSMINUS'''
    p[0] = p[1]

def p_postfix_operator(p):
    '''postfix_operator : PLUSPLUS
                        | MINUSMINUS'''
    p[0] = p[1]

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
    p[0] = p[1]

def p_literal(p):
    '''literal : integer_literal
               | float_literal
               | boolean_literal
               | string_literal'''
    p[0] = p[1]

def p_integer_literal(p):
    '''integer_literal : INTEGER'''
    p[0] = p[1]

def p_float_literal(p):
    '''float_literal : FLOAT'''
    p[0] = p[1]

def p_boolean_literal(p):
    '''boolean_literal : TRUE
                       | FALSE
                       | ZERO
                       | ONE'''
    p[0] = p[1]

def p_string_literal(p):
    '''string_literal : STRING'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = None

# 错误处理
def p_error(p):
    print(f"Syntax error at '{p.value}'")

# 构建解析器
parser = yacc.yacc()

# 测试解析器
data = '''
#include <iostream>
int main() {
    int a = 5;
    if (a > 0) {
        a++;
    }
    return 0;
}
'''

result = parser.parse(data)
print(result)