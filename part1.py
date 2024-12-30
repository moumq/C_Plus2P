import os
import subprocess

def main():
    while True:
        file_path = input("请输入需要分析的文件路径（输入'quit'退出）：").strip()
        if file_path.lower() == 'quit':
            print("退出程序。")
            break

        if not os.path.isfile(file_path):
            print(f"错误：文件 '{file_path}' 不存在。")
            continue

        abs_file_path = os.path.abspath(file_path)

        print("执行词法分析...")
        subprocess.run(['python', './src/lex.py', abs_file_path])

        print("\n执行语法分析...")
        subprocess.run(['python', './src/yacc.py', abs_file_path])

if __name__ == '__main__':
    main()