import getpass
import socket
import shlex
import sys

username = getpass.getuser()
hostname = socket.gethostname()
current_dir = "~"

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
