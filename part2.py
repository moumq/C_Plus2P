# coding=utf-8
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from compile import Compiler

def main():
    if len(sys.argv) != 1:
        print("参数数量错误。")
        return

    in_file_path = input("please input the c file: ")
    in_file_dir, in_file_name = os.path.split(in_file_path)
    out_file_name = '.'.join(in_file_name.split('.')[:-1]) + '.py'
    out_file_path = os.path.join(in_file_dir, out_file_name)
    translator = Compiler()
    translator.compilec(in_file_path, out_file_path)
    print(f"compile succeed :{out_file_path}")

if __name__ == '__main__':
    main()