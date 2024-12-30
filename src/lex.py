import ply.lex as lex
from ply.lex import TOKEN
import sys


reserved = {
    'switch': 'SWITCH',
    'restrict': 'RESTRICT',
    'sizeof': 'SIZEOF',
    'typedef': 'TYPEDEF',
    'union': 'UNION',
    'break': 'BREAK',
    'return': 'RETURN',
    'goto': 'GOTO',
    'enum': 'ENUM',
    'char': 'CHAR',
    'volatile': 'VOLATILE',
    'unsigned': 'UNSIGNED',
    'extern': 'EXTERN',
    'while': 'WHILE',
    'case': 'CASE',
    'short': 'SHORT',
    'inline': 'INLINE',
    'float': 'FLOAT',
    'for': 'FOR',
    'signed': 'SIGNED',
    'default': 'DEFAULT',
    'register': 'REGISTER',
    'long': 'LONG',
    'static': 'STATIC',
    'void': 'VOID',
    'auto': 'AUTO',
    'bool': 'BOOL',
    'continue': 'CONTINUE',
    'int': 'INT',
    'do': 'DO',
    'else': 'ELSE',
    'double': 'DOUBLE',
    'struct': 'STRUCT',
    'if': 'IF',
    'const': 'CONST',
}


tokens = (
    'PTR_OP',
    'LEFT_OP',
    'ADD_ASSIGN',
    'SUB_ASSIGN',
    'RIGHT_OP',
    'DIV_ASSIGN',
    'MOD_ASSIGN',
    'ELLIPSIS',
    'IDENTIFIER',
    'EQ_OP',
    'DEC_OP',
    'MUL_ASSIGN',
    'NE_OP',
    'AND_ASSIGN',
    'OR_OP',
    'GE_OP',
    'LE_OP',
    'STRING_LITERAL',
    'INC_OP',
    'XOR_ASSIGN',
    'OR_ASSIGN',
    'CONSTANT',
    'RIGHT_ASSIGN',
    'LEFT_ASSIGN',
    'AND_OP',
)



literals = ';,:=.&![]{}~()+-*/%><^|?'

t_ELLIPSIS = r'\.\.\.'
t_RIGHT_ASSIGN = r'>>='
t_LEFT_ASSIGN = r'<<='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_XOR_ASSIGN = r'\^='
t_OR_ASSIGN = r'\|='
t_RIGHT_OP = r'>>'
t_LEFT_OP = r'<<'
t_INC_OP = r'\+\+'
t_DEC_OP = r'--'
t_PTR_OP = r'->'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='

# 数字 - 十进制
D = r'[0-9]'
# 数字 - 十六进制
H = r'[0-9a-fA-F]'
# 下划线与字母
L = r'([_a-zA-Z])'
# 科学计数法后缀
E = r'[Ee][+-]?[0-9]+'
# 浮点数修饰符
FS = r'(f|F|l|L)'
# 整型数修饰符
IS = r'(u|U|l|L)*'

# 标识符
identifier = r'(%s(%s|%s)*)' % (L, D, L)
# 布尔
boolean = r'(true|false)'
# 整型数字
integer = r'(0?%s+%s?|0[xX]%s+%s?|%s+%s%s?)' % (D, IS, H, IS, D, E, FS)
# 浮点数字（小数）
decimal = r'((%s+\.%s*(%s)?%s?)|(%s*\.%s+(%s)?%s?))' % (D, D, E, FS, D, D, E, FS)
# 字符
char = r'(\'(\\.|[^\\\'])+\')'
# 常量
constant = r'(%s|%s|%s|%s)' % (decimal, integer, char, boolean)
# 字符串原文
string_literal = r'"(\\.|[^\\"])*"'


# 错误处理
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

@TOKEN(constant)
def t_CONSTANT(t):
    return t

# 空白字符定义
t_ignore = ' \t\v\f'

@TOKEN(string_literal)
def t_STRING_LITERAL(t):
    return t

@TOKEN(identifier)
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# 注释过滤
def t_COMMENT(t):
    r'//[^\n]*'
    pass

# 行号追踪
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


tokens += tuple(reserved.values())
# 构建词法分析器
lexer = lex.lex()

def calculate_position(source_text, token):
    """
    Calculate the position of a token within its line in the source text.
    """
    last_line_break = source_text.rfind('\n', 0, token.lexpos)
    position = token.lexpos - (last_line_break + 1) + 1
    return position


def analyze_file(file_path):
    """
    Analyze the content of a file, tokenize it, and display tokens with their positions.
    """
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            lex.input(file_content)
            while (current_token := lexer.token()) is not None:
                print(current_token, calculate_position(file_content, current_token))
    except FileNotFoundError:
        print(f"Error: Unable to locate the file '{file_path}'.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python lex.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_file(file_path)
