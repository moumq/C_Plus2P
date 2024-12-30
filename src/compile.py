import copy
import re
from tree import internode, exnode
from yacc import parser
import os
# 优化生成代码的风格



def handle_include(include_path, folder):
    """处理 #include 指令"""
    if include_path[0] == '"' and include_path[-1] == '"':
        # 对于自定义头文件，返回完整路径
        return os.path.join(folder, include_path[1:-1])  
    elif include_path[0] == '<' and include_path[-1] == '>':
        # 对于标准库头文件，返回 None 以跳过处理
        return None
    else:
        raise KeyError("Invalid include path")

def handle_macros(lines, folder):
    """ 处理宏定义和宏包含 """
    macro_define_list = []
    macro_include_list = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if len(line) <= 0:
            lines.pop(index)
            continue
        if line[0] == '#':
            words = line[1:].strip().split(' ', 2)
            try:
                # define 识别
                if words[0] == 'define':
                    macro_define_list.append((words[1], words[2]))
                # include 识别
                elif words[0] == 'include':
                    if words[1][0] == '"' and words[1][-1] == '"':
                        macro_include_list.append(os.path.join(folder, words[1][1:-1]))
                    elif words[1][0] == '<' and words[1][-1] == '>':
                        macro_include_list.append(words[1])  # Add standard library includes
                    else:
                        raise KeyError
                else:
                    raise KeyError
            except KeyError:
                return False, f'无效的预处理命令"{line}"，位于文件"{folder}"'
            lines.pop(index)
            continue
        index += 1
    return macro_define_list, macro_include_list, lines

def handle_precompile(filename):
    """预处理文件"""
    folder = os.path.dirname(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.read().split('\n')
    except FileNotFoundError:
        return False, f'无法打开文件"{filename}"'

    # 处理宏定义和宏包含
    macro_define_list, macro_include_list, lines = handle_macros(lines, folder)

    # 处理 define 替换
    s = '\n'.join(lines)
    for m in macro_define_list:
        s = re.sub(m[0], m[1], s)

    # 处理 include 替换
    includes_content = ''
    for m in macro_include_list:
        inc_path = handle_include(m, folder)
        if inc_path:
            # 如果返回值不是 None，表示这是一个有效的文件路径
            inc = handle_precompile(inc_path)
            if inc[0]:
                includes_content += inc[1]
            else:
                return inc
        # 如果是标准库头文件 (None)，则不进行任何操作

    return True, includes_content + s + '\n'

def optimize(s):
    sstr = ''
    i = 0
    while i < len(s):
        match s[i]:
            case '=':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' == '
                    i += 2
                else:
                    sstr += ' = '
                    i += 1
            case '!':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' != '
                    i += 2
                else:
                    sstr += '!'
                    i += 1
            case '>':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' >= '
                    i += 2
                else:
                    sstr += ' > '
                    i += 1
            case '<':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' <= '
                    i += 2
                else:
                    sstr += ' < '
                    i += 1
            case '+':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' += '
                    i += 2
                else:
                    sstr += ' + '
                    i += 1
            case '*':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' *= '
                    i += 2
                else:
                    sstr += ' * '
                    i += 1
            case '/':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' /= '
                    i += 2
                else:
                    sstr += ' / '
                    i += 1
            case '-':
                if i + 1 < len(s) and s[i + 1] == '=':
                    sstr += ' -= '
                    i += 2
                else:
                    if not s[i + 1].isdigit():  # Check if next char is not a digit
                        sstr += ' - '
                        i += 1
                    else:
                        sstr += s[i]
                        i += 1
            case "'":
                # Handle single quotes
                tmp = s.find("'", i + 1)
                sstr += s[i:tmp + 1]
                i = tmp + 1
            case '"':
                # Handle double quotes
                next_quote = s.find('"', i + 1)
                sstr += s[i:next_quote + 1]
                i = next_quote + 1
            case ',':
                # Handle commas
                sstr += ', '
                i += 1
            case _:
                # Handle any other characters
                sstr += s[i]
                i += 1

    return sstr
# 格式化并缩进
def formatIndent(item, rank=-1):
    INDENT_STRING = '    '
    
    def format_single_item(item):
        """ 格式化单一项并处理一些特别情况 """
        item = optimize(item)
        if '(' not in item and ' ' not in item and '=' not in item and item != '' and item not in ['break', 'continue', 'pass', 'else:', 'if', 'return']:
            item += ' = None'
        return item
    
    if isinstance(item, str):
        return INDENT_STRING * rank + format_single_item(item)
    
    if isinstance(item, list):
        lines = [formatIndent(i, rank + 1) for i in item]
        return '\n'.join(lines)


tail = """
if __name__ == "__main__":
    main_0()
"""

# C 中的gets函数
gets_py='''
def gets_0(s):
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c
'''

# C 中的printf函数
printf_py = '''
def printf_0(format, *args):
    new_args = []
    for arg in args:
        if type(arg) == list:
            s = ''
            for c in arg:
                if c == None:
                    break
                s += c
            arg = s
        new_args.append(arg) 
    print(format % tuple(new_args), end='')
'''
# C 中的atoi函数
atoi_py = '''
def atoi_0(s):
    if isinstance(s, str):
        return int(s)
    else:
        sum = 0
        for i in s:
            if i is None:
                break
            sum *= 10
            sum += int(i)
        return sum
'''

# C 中的atof函数
atof_py = '''
def atof_0(s):
    if isinstance(s, str):
        return int(s)
    else:
        mstr = ''
        for i in s:
            if i is None:
                break
            mstr += i
        return float(mstr)
'''

# C中的system函数
system_py = '''
def system_0(s):
    if not isinstance(s, str):
        s = filter(lambda x: x != 0, s)
        s = ''.join(s)
    import os
    os.system(s)
'''

# C 中的strlen函数，这里通过None判断数组末尾
strlen_py = '''
def strlen_0(s):
    if isinstance(s, str):
        return len(s)
    else:
        _len = 0
        for i in s:
            if i is None:
                break
            _len += 1
        return _len
'''


some_functions = [printf_py, system_py, atoi_py, atof_py,strlen_py, gets_py]

class Compiler:
    def __init__(self):
        self.funcs = []
        self.decls = []
        self.globals = []
        self.var_table = {}
        self.head = "".join(some_functions) + '\n'
        self.tail = tail

    def compilec(self, input_file_name, output_file_name):
        try:
            success, file_content = handle_precompile(input_file_name)
            if not success:
                print(file_content)
                return
            tree = parser.parse(file_content)
            raw_outcome = self.process(tree)
            out = self.head + formatIndent(raw_outcome) + self.tail
            with open(output_file_name, 'w+', encoding='utf-8') as output_file:
                output_file.write(out)
            print(f'{input_file_name} is compiled into {output_file_name} 。')
        except Exception as e:
            print(str(e))

    def flag_calc(self, tree, flag_list):
        if tree.key == 'struct_or_union_spec':
            return tree.children[1].value
        return next((flag for flag in flag_list if flag), '')

    def leaf_str(self, tree):
        translations = {
            ';': [''],
            '&&': [' and '],
            '||': [' or '],
            '!': ['not '],
            'true': ['True'],
            'false': ['False'],
            'struct': ['class']
        }
        return translations.get(tree.value, [tree.value])

    def traverse(self, tree, stack, type):
        stack.append(tree.key)
        code_list, flag_list = [], []

        if isinstance(tree, exnode):
            stack.pop()
            return self.leaf_str(tree), ''
        
        for child in tree.children:
            code, flag = self.traverse(child, stack, type)
            code_list.append(code)
            flag_list.append(flag)
        
        flag_to_upper = self.flag_calc(tree, flag_list)
        pycode = self.code_compose(tree, code_list, flag_to_upper)
        stack.pop()
        return pycode, flag_to_upper

    def process(self, tree):
        def pick_out(tree):
            if tree.key == 'func_def':
                self.funcs.append(tree)
            else:
                self.decls.append(tree)

        while tree.key == 'program':
            if len(tree.children) == 2:
                pick_out(tree.children[1].children[0])
                tree = tree.children[0]
            else:
                pick_out(tree.children[0].children[0])
                break

        self.decls = list(reversed(self.decls))
        code_list = []

        for decl in self.decls:
            if self.is_func_decl(decl):
                continue
            self.decl_extract(decl)
            code, flag = self.traverse(decl, [], 'declaration')
            code_list.extend(code)
            code_list.append('')

        for func in self.funcs:
            table_copy = copy.deepcopy(self.var_table)
            self.name_replace(func)
            self.var_table = table_copy
            code, flag = self.traverse(func, [], 'function')
            code_list.extend(code)
            code_list.append('')

        return code_list

    def is_func_decl(self, tree):
        for child in tree.children:
            if isinstance(child, exnode):
                return False
            if child.key == 'direct_declr':
                return len(child.children) > 1 and isinstance(child.children[1], exnode) and child.children[1].value == '('
            if self.is_func_decl(child):
                return True
        return False

    def decl_extract(self, tree):
        if tree.key == 'struct_or_union_spec' or isinstance(tree, exnode):
            return
        for child in tree.children:
            if child.key == 'IDENTIFIER':
                alias = f"{child.value}_0"
                self.globals.append(alias)
                self.var_table[child.value] = [(alias, True)]
                child.value = alias
            else:
                self.decl_extract(child)

    def name_replace(self, tree, is_declr=False):
        if isinstance(tree, internode):
            if tree.key == 'declr':
                for child in tree.children:
                    self.name_replace(child, True)
            elif tree.key == 'prim_expr':
                for child in tree.children:
                    self.name_replace(child, False)
            elif tree.key == 'struct_or_union_spec':
                return
            elif tree.key == 'post_expr' and len(tree.children) == 3 and isinstance(tree.children[2], exnode) and tree.children[2].key == 'IDENTIFIER':
                for child in tree.children[:2]:
                    self.name_replace(child, False)
            elif tree.key in ['iter_stmt', 'sel_stmt']:
                table_copy = copy.deepcopy(self.var_table)
                for child in tree.children:
                    self.name_replace(child, is_declr)
                self.var_table = table_copy
            else:
                for child in tree.children:
                    self.name_replace(child, is_declr)
        else:
            if tree.key != 'IDENTIFIER':
                return
            if tree.value in self.var_table:
                table = self.var_table[tree.value]
                if is_declr:
                    alias = f"{tree.value}_{len(table)}"
                    table.append((alias, False))
                    tree.value = alias
                else:
                    tree.value = table[-1][0] if table else f"{tree.value}_0"
            else:
                alias = f"{tree.value}_0"
                self.var_table[tree.value] = [(alias, False)]
                tree.value = alias

    def code_compose(self, tree, code_list, flag):
        if tree.key == 'unary_expr' and isinstance(tree.children[0], exnode):
            if tree.children[0].value == '++':
                return [f"{code_list[1][0]} = {code_list[1][0]} + 1"]
            if tree.children[0].value == '--':
                return [f"{code_list[1][0]} = {code_list[1][0]} - 1"]

        elif tree.key == 'post_expr' and len(tree.children) == 2:
            if tree.children[1].value == '--':
                return [f"{code_list[0][0]} = {code_list[0][0]} - 1"]
            if tree.children[1].value == '++':
                return [f"{code_list[0][0]} = {code_list[0][0]} + 1"]

        elif tree.key == 'jump_stmt' and tree.children[0].key == 'return':
            return ['return'] if len(tree.children) == 2 else [f"{code_list[0][0]} {code_list[1][0]}"]

        elif tree.key == 'sel_stmt':
            if len(tree.children) == 5:
                return [f"if {code_list[2][0]}:", code_list[4]]
            if len(tree.children) == 7:
                return [f"if {code_list[2][0]}:", code_list[4], 'else:', code_list[6]]

        elif tree.key == 'iter_stmt':
            if tree.children[0].value == 'while':
                return [f"while {code_list[2][0]}:", code_list[4]]
            if len(tree.children) == 7:
                return [code_list[2][0], f"while {code_list[3][0]}:", code_list[6], code_list[4]]

        elif tree.key == 'block_item_list':
            return [c for code in code_list for c in code]

        elif tree.key == 'comp_stmt':
            return code_list[1] if len(tree.children) == 3 else ['pass']

        elif tree.key == 'func_def':
            if len(tree.children) == 3:
                function_body = [f"global {var}" for var in self.globals] + code_list[2]
                return [f"def {code_list[1][0]}:", function_body]

        elif tree.key == 'param_decl' and len(tree.children) == 2:
            return code_list[1]

        elif tree.key == 'direct_declr' and len(tree.children) == 3 and tree.children[1].value == '[':
            return [code_list[0][0]]

        elif tree.key == 'init_decl_list':
            return [code_list[0][0], code_list[2][0]] if len(tree.children) > 1 else code_list[0]

        elif tree.key == 'struct_or_union_spec' and len(tree.children) == 2:
            return code_list[1]

        elif tree.key == 'struct_or_union_spec' and len(tree.children) == 5:
            return [f"{code_list[0][0]} {code_list[1][0]}:", code_list[3]]

        elif tree.key == 'struct_decl_list':
            return [c for code in code_list for c in code]

        elif tree.key in ['decl', 'struct_decl']:
            if len(tree.children) == 3 and flag == '':
                return code_list[1]
            elif len(tree.children) == 3 and flag != '':
                result = code_list[0] if flag != code_list[0][0] else []
                for class_obj in code_list[1]:
                    result.append(f"{class_obj} = {flag}()")
                if len(result) == 1 and '=' in result[0]:
                    tmp = result[0]
                    tmp_2 = tmp.split('=')[2].lstrip()
                    tmp = f"{tmp.split('=')[0]} = {tmp.split('=')[1]}"
                    tmp = f"{tmp[:tmp.find('[') + 1]}{tmp_2} for i in range({tmp[tmp.find('*') + 1:]})]"
                    result = [tmp.rstrip()]
                return result
            elif len(tree.children) == 2:
                return code_list[0]

        elif tree.key == 'direct_declr' and len(tree.children) == 4 and isinstance(tree.children[2], internode) and tree.children[2].key == 'assign_expr':
            return [f"{code_list[0][0]} = [None] * {code_list[2][0]}"]

        elif tree.key == 'init_decl' and len(tree.children) == 3 and '[' in code_list[0][0]:
            tmp = code_list[0][0]
            left = tmp[:tmp.find('[') - 1]
            length = code_list[0][0].split('*')[1]

            if '"' in code_list[2][0]:
                tmp = code_list[2][0].strip('"')
                result = [f"{left} = [None] * {length}"]
                result.extend([f"{left}[{i}] = '{c}'" for i, c in enumerate(tmp)])
                return result
            else:
                tmp = code_list[2][0].split(',')
                result = [f"{left} = [None] * {length}"]
                result.extend([f"{left}[{i}] = {c}" for i, c in enumerate(tmp)])
                return result

        elif tree.key == 'init' and len(tree.children) == 3:
            return code_list[1]

        else:
            if all(len(code) == 1 for code in code_list):
                return ["".join(code[0] for code in code_list)]
            return [c for code in code_list for c in code]

