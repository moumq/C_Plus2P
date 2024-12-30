
import sys
import re
import ply.yacc as yacc

import json
from tree import internode, exnode ,node
reserved_list = ['true', 'false']

from lex import tokens, identifier

# 定义自定义的 JSONEncoder，用于处理 internode 和 exnode 类
class ASTEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, internode):
            return {
                "type": obj.key,
                "children": [self.default(child) if isinstance(child, node) else str(child) for child in obj.children]
            }
        elif isinstance(obj, exnode):
            return {
                "type": obj.key,
                "value": obj.value
            }
        return super().default(obj)
    

def p_program(p):
    ''' program : ext_decl
                | program ext_decl '''
    p[0] = internode('program', p[1:])


def p_ext_decl(p):
    ''' ext_decl : func_def
                 | decl '''
    p[0] = internode('ext_decl', p[1:])


def p_decl(p):
    ''' decl : decl_specs ';'
             | decl_specs init_decl_list ';' '''
    p[0] = internode('decl', p[1:])


def p_init_decl_list(p):
    ''' init_decl_list : init_decl
                       | init_decl_list ',' init_decl '''
    p[0] = internode('init_decl_list', p[1:])


def p_init_decl(p):
    ''' init_decl : declr
                  | declr '=' init '''
    p[0] = internode('init_decl', p[1:])


def p_decl_specs(p):
    ''' decl_specs : stor_class_spec
                  | stor_class_spec decl_specs
                  | type_spec
                  | type_spec decl_specs
                  | type_qual
                  | type_qual decl_specs
                  | func_spec
                  | func_spec decl_specs '''
    p[0] = internode('decl_specs', p[1:])


def p_stor_class_spec(p):
    ''' stor_class_spec : TYPEDEF
                        | EXTERN
                        | STATIC
                        | AUTO
                        | REGISTER '''
    p[0] = internode('stor_class_spec', p[1:])


def p_func_spec(p):
    ''' func_spec : INLINE '''
    p[0] = internode('func_spec', p[1:])


def p_type_spec(p):
    ''' type_spec : VOID
                  | CHAR
                  | SHORT
                  | INT
                  | LONG
                  | FLOAT
                  | DOUBLE
                  | SIGNED
                  | UNSIGNED
                  | BOOL
                  | struct_or_union_spec
                  | enum_spec '''
    p[0] = internode('type_spec', p[1:])


def p_type_qual(p):
    ''' type_qual : CONST
                  | RESTRICT
                  | VOLATILE '''
    p[0] = internode('type_qual', p[1:])


def p_enum_spec(p):
    ''' enum_spec : ENUM '{' enum_list '}'
                  | ENUM IDENTIFIER '{' enum_list '}'
                  | ENUM '{' enum_list ',' '}'
                  | ENUM IDENTIFIER '{' enum_list ',' '}'
                  | ENUM IDENTIFIER '''
    if not p[2] == '{' and not p[2] in reserved_list:
        p[2] = exnode('IDENTIFIER', p[2])
    p[0] = internode('enum_spec', p[1:])


def p_enum_list(p):
    ''' enum_list : enum
                  | enum_list ',' enum '''
    p[0] = internode('enum_list', p[1:])


def p_enum(p):
    ''' enum : IDENTIFIER
             | IDENTIFIER '=' const_expr '''
    if not p[1] in reserved_list:
        p[1] = exnode('IDENTIFIER', p[1])
    p[0] = internode('enum', p[1:])


def p_struct_or_union_spec(p):
    ''' struct_or_union_spec : struct_or_union IDENTIFIER '{' struct_decl_list '}'
                             | struct_or_union '{' struct_decl_list '}'
                             | struct_or_union IDENTIFIER '''
    if not p[2] == '{' and not p[2] in reserved_list:
        p[2] = exnode('IDENTIFIER', p[2])
    p[0] = internode('struct_or_union_spec', p[1:])


def p_struct_or_union(p):
    ''' struct_or_union : STRUCT
                        | UNION '''
    p[0] = internode('struct_or_union', p[1:])


def p_struct_decl_list(p):
    ''' struct_decl_list : struct_decl
                         | struct_decl_list struct_decl '''
    p[0] = internode('struct_decl_list', p[1:])


def p_struct_decl(p):
    ''' struct_decl : spec_qual_list struct_declr_list ';' '''
    p[0] = internode('struct_decl', p[1:])


def p_spec_qual_list(p):
    ''' spec_qual_list : type_spec spec_qual_list
                       | type_spec
                       | type_qual spec_qual_list
                       | type_qual '''
    p[0] = internode('spec_qual_list', p[1:])


def p_struct_declr_list(p):
    ''' struct_declr_list : struct_declr
                          | struct_declr_list ',' struct_declr '''
    p[0] = internode('struct_declr_list', p[1:])


def p_struct_declr(p):
    ''' struct_declr : declr
                     | ':' const_expr
                     | declr ':' const_expr '''
    p[0] = internode('struct_declr', p[1:])


def p_declr(p):
    ''' declr : ptr direct_declr
              | direct_declr '''
    p[0] = internode('declr', p[1:])


def p_ptr(p):
    ''' ptr : '*'
            | '*' type_qual_list
            | '*' ptr
            | '*' type_qual_list ptr '''
    p[0] = internode('ptr', p[1:])


def p_type_qual_list(p):
    ''' type_qual_list : type_qual
                       | type_qual_list type_qual '''
    p[0] = internode('type_qual_list', p[1:])


def p_direct_declr(p):
    ''' direct_declr : IDENTIFIER
                     | '(' declr ')'
                     | direct_declr '[' type_qual_list assign_expr ']'
                     | direct_declr '[' type_qual_list ']'
                     | direct_declr '[' assign_expr ']'
                     | direct_declr '[' STATIC type_qual_list assign_expr ']'
                     | direct_declr '[' type_qual_list STATIC assign_expr ']'
                     | direct_declr '[' type_qual_list '*' ']'
                     | direct_declr '[' '*' ']'
                     | direct_declr '[' ']'
                     | direct_declr '(' param_type_list ')'
                     | direct_declr '(' id_list ')'
                     | direct_declr '(' ')' '''
    if len(p) == 2 and not p[1] in reserved_list:
        p[1] = exnode('IDENTIFIER', p[1])
    p[0] = internode('direct_declr', p[1:])


def p_id_list(p):
    ''' id_list : IDENTIFIER
                | id_list ',' IDENTIFIER '''
    if len(p) == 2 and not p[1] in reserved_list:
        p[1] = exnode('IDENTIFIER', p[1])
    elif len(p) == 4 and not p[3] in reserved_list:
        p[3] = exnode('IDENTIFIER', p[3])
    p[0] = internode('id_list', p[1:])


def p_assign_expr(p):
    ''' assign_expr : cond_expr
                    | unary_expr assign_op assign_expr '''
    p[0] = internode('assign_expr', p[1:])


def p_assign_op(p):
    ''' assign_op : '='
                  | MUL_ASSIGN
                  | DIV_ASSIGN
                  | MOD_ASSIGN
                  | ADD_ASSIGN
                  | SUB_ASSIGN
                  | LEFT_ASSIGN
                  | RIGHT_ASSIGN
                  | AND_ASSIGN
                  | XOR_ASSIGN
                  | OR_ASSIGN '''
    p[0] = internode('assign_op', p[1:])


def p_const_expr(p):
    ''' const_expr : cond_expr '''
    p[0] = internode('const_expr', p[1:])


def p_cond_expr(p):
    ''' cond_expr : log_or_expr
                  | log_or_expr '?' expr ':' cond_expr '''
    p[0] = internode('cond_expr', p[1:])


def p_log_or_expr(p):
    ''' log_or_expr : log_and_expr
                    | log_or_expr OR_OP log_and_expr '''
    p[0] = internode('log_or_expr', p[1:])


def p_log_and_expr(p):
    ''' log_and_expr : incl_or_expr
                     | log_and_expr AND_OP incl_or_expr '''
    p[0] = internode('log_and_expr', p[1:])


def p_incl_or_expr(p):
    ''' incl_or_expr : excl_or_expr
                     | incl_or_expr '|' excl_or_expr '''
    p[0] = internode('incl_or_expr', p[1:])


def p_excl_or_expr(p):
    ''' excl_or_expr : and_expr
                     | excl_or_expr '^' and_expr '''
    p[0] = internode('excl_or_expr', p[1:])


def p_and_expr(p):
    ''' and_expr : eq_expr
                 | and_expr '&' eq_expr '''
    p[0] = internode('and_expr', p[1:])


def p_eq_expr(p):
    ''' eq_expr : rel_expr
                | eq_expr EQ_OP rel_expr
                | eq_expr NE_OP rel_expr '''
    p[0] = internode('eq_expr', p[1:])


def p_rel_expr(p):
    ''' rel_expr : shift_expr
                 | rel_expr '<' shift_expr
                 | rel_expr '>' shift_expr
                 | rel_expr LE_OP shift_expr
                 | rel_expr GE_OP shift_expr '''
    p[0] = internode('rel_expr', p[1:])


def p_shift_expr(p):
    ''' shift_expr : add_expr
                   | shift_expr LEFT_OP add_expr
                   | shift_expr RIGHT_OP add_expr '''
    p[0] = internode('shift_expr', p[1:])


def p_add_expr(p):
    ''' add_expr : mult_expr
                 | add_expr '+' mult_expr
                 | add_expr '-' mult_expr '''
    p[0] = internode('add_expr', p[1:])


def p_mult_expr(p):
    ''' mult_expr : cast_expr
                  | mult_expr '*' cast_expr
                  | mult_expr '/' cast_expr
                  | mult_expr '%' cast_expr '''
    p[0] = internode('mult_expr', p[1:])


def p_cast_expr(p):
    ''' cast_expr : unary_expr
                  | '(' type_name ')' cast_expr '''
    p[0] = internode('cast_expr', p[1:])


def p_unary_expr(p):
    ''' unary_expr : post_expr
                   | INC_OP unary_expr
                   | DEC_OP unary_expr
                   | unary_op cast_expr
                   | SIZEOF unary_expr
                   | SIZEOF '(' type_name ')' '''
    p[0] = internode('unary_expr', p[1:])


def p_unary_op(p):
    ''' unary_op : '&'
                 | '*'
                 | '+'
                 | '-'
                 | '~'
                 | '!' '''
    p[0] = internode('unary_op', p[1:])


def p_post_expr(p):
    ''' post_expr : prim_expr
                  | post_expr '[' expr ']'
                  | post_expr '(' ')'
                  | post_expr '(' arg_expr_list ')'
                  | post_expr '.' IDENTIFIER
                  | post_expr PTR_OP IDENTIFIER
                  | post_expr INC_OP
                  | post_expr DEC_OP
                  | '(' type_name ')' '{' init_list '}'
                  | '(' type_name ')' '{' init_list ',' '}' '''
    if len(p) == 4 and not p[2] == '(' and not p[3] in reserved_list:
        p[3] = exnode('IDENTIFIER', p[3])
    p[0] = internode('post_expr', p[1:])


def p_prim_expr(p):
    ''' prim_expr : IDENTIFIER
                  | CONSTANT
                  | STRING_LITERAL
                  | '(' expr ')' '''
    if re.match(r'(([_a-zA-Z])([0-9]|([_a-zA-Z]))*)', p[1]) and not p[1] in reserved_list:
        p[1] = exnode('IDENTIFIER', str(p[1]))
    p[0] = internode('prim_expr', p[1:])


def p_expr(p):
    ''' expr : assign_expr
             | expr ',' assign_expr '''
    p[0] = internode('expr', p[1:])


def p_type_name(p):
    ''' type_name : spec_qual_list
                  | spec_qual_list abs_declr '''
    p[0] = internode('type_name', p[1:])


def p_abs_declr(p):
    ''' abs_declr : ptr
                  | direct_abs_declr
                  | ptr direct_abs_declr '''
    p[0] = internode('abs_declr', p[1:])


def p_direct_abs_declr(p):
    ''' direct_abs_declr : '(' abs_declr ')'
                         | '[' ']'
                         | '[' assign_expr ']'
                         | direct_abs_declr '[' ']'
                         | direct_abs_declr '[' assign_expr ']'
                         | '[' '*' ']'
                         | direct_abs_declr '[' '*' ']'
                         | '(' ')'
                         | '(' param_type_list ')'
                         | direct_abs_declr '(' ')'
                         | direct_abs_declr '(' param_type_list ')' '''
    p[0] = internode('direct_abs_declr', p[1:])


def p_param_type_list(p):
    ''' param_type_list : param_list
                        | param_list ',' ELLIPSIS '''
    p[0] = internode('param_type_list', p[1:])


def p_param_list(p):
    ''' param_list : param_decl
                   | param_list ',' param_decl '''
    p[0] = internode('param_list', p[1:])


def p_param_decl(p):
    ''' param_decl : decl_specs declr
                   | decl_specs abs_declr
                   | decl_specs '''
    p[0] = internode('param_decl', p[1:])


def p_arg_expr_list(p):
    ''' arg_expr_list : assign_expr
                      | arg_expr_list ',' assign_expr '''
    p[0] = internode('arg_expr_list', p[1:])


def p_init_list(p):
    ''' init_list : init
                  | desig init
                  | init_list ',' init
                  | init_list ',' desig init '''
    p[0] = internode('init_list', p[1:])


def p_init(p):
    ''' init : assign_expr
             | '{' init_list '}'
             | '{' init_list ',' '}' '''
    p[0] = internode('init', p[1:])


def p_desig(p):
    ''' desig : desig_list '=' '''
    p[0] = internode('desig', p[1:])


def p_desig_list(p):
    ''' desig_list : desig
                   | desig_list desig '''
    p[0] = internode('desig_list', p[1:])


def p_desig(p):
    ''' desig : '[' const_expr ']'
              | '.' IDENTIFIER '''
    if len(p) == 3 and not p[2] in reserved_list:
        p[2] = exnode('IDENTIFIER', p[2])
    p[0] = internode('desig', p[1:])


def p_func_def(p):
    ''' func_def : decl_specs declr decl_list comp_stmt
                 | decl_specs declr comp_stmt '''
    p[0] = internode('func_def', p[1:])


def p_decl_list(p):
    ''' decl_list : decl
                  | decl_list decl '''
    p[0] = internode('decl_list', p[1:])


def p_comp_stmt(p):
    ''' comp_stmt : '{' '}'
                  | '{' block_item_list '}' '''
    p[0] = internode('comp_stmt', p[1:])


def p_block_item_list(p):
    ''' block_item_list : block_item
                        | block_item_list block_item '''
    p[0] = internode('block_item_list', p[1:])


def p_block_item(p):
    ''' block_item : decl
                   | stmt '''
    p[0] = internode('block_item', p[1:])


def p_stmt(p):
    ''' stmt : labeled_stmt
             | comp_stmt
             | expr_stmt
             | sel_stmt
             | iter_stmt
             | jump_stmt '''
    p[0] = internode('stmt', p[1:])


def p_labeled_stmt(p):
    ''' labeled_stmt : IDENTIFIER ':' stmt
                     | CASE const_expr ':' stmt
                     | DEFAULT ':' stmt '''
    if len(p) == 4 and not p[1] == 'default' and not p[1] in reserved_list:
        p[1] = exnode('IDENTIFIER', p[1])
    p[0] = internode('labeled_stmt', p[1:])


def p_expr_stmt(p):
    ''' expr_stmt : ';'
                  | expr ';' '''
    p[0] = internode('expr_stmt', p[1:])


def p_sel_stmt(p):
    ''' sel_stmt : IF '(' expr ')' stmt ELSE stmt
                 | IF '(' expr ')' stmt
                 | SWITCH '(' expr ')' stmt '''
    p[0] = internode('sel_stmt', p[1:])


def p_iter_stmt(p):
    ''' iter_stmt : WHILE '(' expr ')' stmt
                  | DO stmt WHILE '(' expr ')' ';'
                  | FOR '(' expr_stmt expr_stmt ')' stmt
                  | FOR '(' expr_stmt expr_stmt expr ')' stmt
                  | FOR '(' decl expr_stmt ')' stmt
                  | FOR '(' decl expr_stmt expr ')' stmt '''
    p[0] = internode('iter_stmt', p[1:])


def p_jump_stmt(p):
    ''' jump_stmt : GOTO IDENTIFIER ';'
                  | CONTINUE ';'
                  | BREAK ';'
                  | RETURN ';'
                  | RETURN expr ';' '''
    if len(p) == 4 and p[1] == 'goto' and not p[2] in reserved_list:
        p[2] = exnode('IDENTIFIER', p[2])
    p[0] = internode('jump_stmt', p[1:])

# 语法分析  错误处理
def p_error(p):
    """日志记录错误信息"""
    error_message = (
        f"❌ [Syntax Error] \n"
        f"   ├── Type    : {p.type}\n"
        f"   ├── Value   : {p.value}\n"
        f"   ├── Line No : {p.lineno}\n"
        f"   └── LexPos  : {p.lexpos}"
    )
    print(error_message)



def convert_to_json(ast):
    """将抽象语法树转换为JSON格式"""
    return json.dumps(ast, cls=ASTEncoder, indent=2)


def parse_file(file_path, parser):
    """解析文件内容并返回解析结果"""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            result = parser.parse(content)
            return result
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")


def start_interactive_mode(parser):
    """启动交互式模式，接受用户输入"""
    print("Enter 'quit' to exit the program.")
    while True:
        try:
            user_input = input('语法分析： ').strip()
            if user_input.lower() == 'quit':
                print("Exiting...")
                break
            result = parse_file(user_input, parser)
            if result:
                print(convert_to_json(result))
        except EOFError:
            break

def analyze_file(file_path):
    """解析文件并输出语法树"""
    result = parse_file(file_path, parser)
    if result:
        print(convert_to_json(result))
        
parser = yacc.yacc()
# 测试程序
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python yacc.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_file(file_path)