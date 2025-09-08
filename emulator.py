import getpass
import socket
import shlex
import sys
import argparse
import os
import json
import base64
from pathlib import Path

username = getpass.getuser()
hostname = socket.gethostname()
current_dir = "~"
vfs_path = None
vfs_data = None

def load_vfs(vfs_file_path):
    global vfs_data
    try:
        with open(vfs_file_path, 'r', encoding='utf-8') as f:
            vfs_data = json.load(f)
        return True
    except FileNotFoundError:
        print(f"Ошибка: VFS файл не найден: {vfs_file_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"Ошибка: неверный формат JSON в VFS файле: {e}")
        return False
    except Exception as e:
        print(f"Ошибка загрузки VFS: {e}")
        return False

def get_vfs_path(path):
    if path.startswith('~'):
        path = path[1:]
    if path.startswith('/'):
        path = path[1:]
    return path.split('/') if path else []

def find_vfs_item(path_parts):
    if not vfs_data:
        return None
    
    current = vfs_data
    for part in path_parts:
        if part == '':
            continue
        if 'children' in current and part in current['children']:
            current = current['children'][part]
        else:
            return None
    return current

def list_vfs_directory(path):
    path_parts = get_vfs_path(path) if path != "~" else []
    item = find_vfs_item(path_parts)
    
    if not item:
        return f"ls: {path}: нет такого файла или каталога"
    
    if item.get('type') != 'directory':
        if item.get('type') == 'file':
            size = len(base64.b64decode(item.get('content', ''))) if item.get('content') else 0
            return f"- {path.split('/')[-1]} ({size} bytes)"
        return f"ls: {path}: не является каталогом"
    
    if 'children' not in item:
        return ""
    
    result = []
    for name, child in item['children'].items():
        if child.get('type') == 'directory':
            result.append(f"d {name}/")
        else:
            size = len(base64.b64decode(child.get('content', ''))) if child.get('content') else 0
            result.append(f"- {name} ({size} bytes)")
    
    return '\n'.join(result)

def change_vfs_directory(path):
    global current_dir
    
    if path == "~" or path == "":
        current_dir = "~"
        return True
    
    if path == "..":
        if current_dir == "~":
            return True
        parts = current_dir.split("/")
        if len(parts) > 1:
            current_dir = "/".join(parts[:-1])
        else:
            current_dir = "~"
        return True
    
    new_path = path
    if current_dir != "~":
        new_path = f"{current_dir}/{path}"
    
    path_parts = get_vfs_path(new_path)
    item = find_vfs_item(path_parts)
    
    if not item:
        print(f"cd: {path}: нет такого файла или каталога")
        return False
    
    if item.get('type') != 'directory':
        print(f"cd: {path}: не является каталогом")
        return False
    
    current_dir = new_path if new_path != "" else "~"
    return True

def save_vfs(save_path):
    if not vfs_data:
        print("Ошибка: VFS не загружена")
        return False
    
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(vfs_data, f, ensure_ascii=False, indent=2)
        print(f"VFS сохранена в {save_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения VFS: {e}")
        return False

def get_prompt():
    return f"{username}@{hostname}:{current_dir}$ "

def parse_command(input_line):
    try:
        return shlex.split(input_line.strip())
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга: {e}")

def get_file_content(path):
    path_parts = get_vfs_path(path)
    item = find_vfs_item(path_parts)
    
    if not item:
        return None
    
    if item.get('type') != 'file':
        return None
    
    content = item.get('content', '')
    if content:
        try:
            return base64.b64decode(content).decode('utf-8')
        except:
            return base64.b64decode(content)
    return ""

def cmd_ls(args):
    if vfs_data:
        path = args[0] if args else current_dir
        result = list_vfs_directory(path)
        print(result)
    else:
        print(f"ls {' '.join(args) if args else ''}")

def cmd_cd(args):
    global current_dir
    if vfs_data:
        path = args[0] if args else "~"
        change_vfs_directory(path)
    else:
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

def cmd_echo(args):
    print(' '.join(args))

def cmd_clear(args):
    os.system('clear' if os.name == 'posix' else 'cls')

def cmd_wc(args):
    if not args:
        print("wc: отсутствует аргумент файла")
        return
    
    if not vfs_data:
        print(f"wc: файл '{args[0]}' не найден (VFS не загружена)")
        return
    
    file_path = args[0]
    if current_dir != "~":
        file_path = f"{current_dir}/{args[0]}"
    
    content = get_file_content(file_path)
    
    if content is None:
        print(f"wc: {args[0]}: нет такого файла или каталога")
        return
    
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except:
            print(f"wc: {args[0]}: не удается прочитать как текст")
            return
    
    lines = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
    words = len(content.split())
    chars = len(content)
    
    print(f"  {lines}  {words} {chars} {args[0]}")

def cmd_touch(args):
    if not args:
        print("touch: отсутствует аргумент файла")
        return
    
    if not vfs_data:
        print("touch: VFS не загружена")
        return
    
    file_name = args[0]
    
    current_path_parts = get_vfs_path(current_dir) if current_dir != "~" else []
    current_item = find_vfs_item(current_path_parts)
    
    if not current_item or current_item.get('type') != 'directory':
        print(f"touch: текущая директория недоступна")
        return
    
    if 'children' not in current_item:
        current_item['children'] = {}
    
    if file_name in current_item['children']:
        print(f"touch: файл '{file_name}' уже существует")
        return
    
    current_item['children'][file_name] = {
        'type': 'file',
        'content': '',
        'permissions': '644'
    }
    
    print(f"touch: файл '{file_name}' создан")

def cmd_chmod(args):
    if len(args) < 2:
        print("chmod: неверное количество аргументов")
        print("Использование: chmod <права> <файл>")
        return
    
    if not vfs_data:
        print("chmod: VFS не загружена")
        return
    
    permissions = args[0]
    file_name = args[1]
    
    if not permissions.isdigit() or len(permissions) != 3:
        print("chmod: неверный формат прав (используйте трёхзначное число)")
        return
    
    file_path = file_name
    if current_dir != "~":
        file_path = f"{current_dir}/{file_name}"
    
    path_parts = get_vfs_path(file_path)
    item = find_vfs_item(path_parts)
    
    if not item:
        print(f"chmod: {file_name}: нет такого файла или каталога")
        return
    
    if item.get('type') not in ['file', 'directory']:
        print(f"chmod: {file_name}: неподдерживаемый тип объекта")
        return
    
    item['permissions'] = permissions
    print(f"chmod: права на '{file_name}' изменены на {permissions}")

def cmd_vfs_save(args):
    if not args:
        print("vfs-save: необходимо указать путь для сохранения")
        return
    save_vfs(args[0])

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
        'echo': cmd_echo,
        'clear': cmd_clear,
        'wc': cmd_wc,
        'touch': cmd_touch,
        'chmod': cmd_chmod,
        'vfs-save': cmd_vfs_save,
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
    
    if args.vfs:
        print(f"\nЗагрузка VFS: {args.vfs}")
        if load_vfs(args.vfs):
            print("VFS успешно загружена")
        else:
            print("Ошибка загрузки VFS, работа в режиме без VFS")
    
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
