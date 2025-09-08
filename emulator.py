import getpass
import socket
import shlex
import sys
import argparse
import os

username = getpass.getuser()
hostname = socket.gethostname()
current_dir = "~"
vfs_path = None

def get_prompt():
    return f"{username}@{hostname}:{current_dir}$ "

def parse_command(input_line):
    try:
        return shlex.split(input_line.strip())
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга: {e}")

def cmd_ls(args):
    print(f"ls {' '.join(args) if args else ''}")

def cmd_cd(args):
    global current_dir
    print(f"cd {' '.join(args) if args else ''}")
    if args:
        if args[0] == "~" or args[0] == "":
            current_dir = "~"
        elif args[0] == "..":
            if current_dir != "~":
                parts = current_dir.split("/")
                if len(parts) > 1:
                    current_dir = "/".join(parts[:-1])
                else:
                    current_dir = "~"
        else:
            if current_dir == "~":
                current_dir = args[0]
            else:
                current_dir = f"{current_dir}/{args[0]}"

def cmd_exit(args):
    print("exit")
    sys.exit(0)

def execute_startup_script(script_path):
    if not os.path.exists(script_path):
        print(f"Ошибка: стартовый скрипт не найден: {script_path}")
        return False
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Ошибка чтения скрипта: {e}")
        return False
    
    for line_num, line in enumerate(lines, 1):
        command = line.strip()
        if not command or command.startswith('#'):
            continue
        
        print(get_prompt() + command)
        
        try:
            args = parse_command(command)
            execute_command(args)
        except ValueError as e:
            print(f"Ошибка в строке {line_num}: {e}")
            return False
        except Exception as e:
            print(f"Ошибка выполнения команды в строке {line_num}: {e}")
            return False
    
    return True

def parse_args():
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки UNIX')
    parser.add_argument('--vfs', type=str, help='Путь к виртуальной файловой системе')
    parser.add_argument('--script', type=str, help='Путь к стартовому скрипту')
    return parser.parse_args()

def print_config(args):
    print("=== Конфигурация эмулятора ===")
    print(f"Пользователь: {username}")
    print(f"Хост: {hostname}")
    print(f"Текущая директория: {current_dir}")
    print(f"VFS путь: {args.vfs if args.vfs else 'не указан'}")
    print(f"Стартовый скрипт: {args.script if args.script else 'не указан'}")
    print("=" * 30)

def execute_command(args):
    if not args:
        return
    command = args[0]
    command_args = args[1:]
    commands = {
        'ls': cmd_ls,
        'cd': cmd_cd,
        'exit': cmd_exit
    }
    if command in commands:
        try:
            commands[command](command_args)
        except Exception as e:
            print(f"Ошибка выполнения команды '{command}': {e}")
    else:
        print(f"bash: {command}: команда не найдена")

def main():
    args = parse_args()
    global vfs_path
    vfs_path = args.vfs
    
    print_config(args)
    
    if args.script:
        print(f"\nВыполнение стартового скрипта: {args.script}")
        if execute_startup_script(args.script):
            print("Стартовый скрипт выполнен успешно\n")
        else:
            print("Ошибка выполнения стартового скрипта")
            sys.exit(1)
    
    try:
        while True:
            try:
                user_input = input(get_prompt())
                if not user_input.strip():
                    continue
                args = parse_command(user_input)
                execute_command(args)
            except ValueError as e:
                print(f"Ошибка: {e}")
            except KeyboardInterrupt:
                print("\n^C")
                continue
            except EOFError:
                print("\nexit")
                break
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
