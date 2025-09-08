CLI программа на Python, эмулятор UNIX-подобных терминалов (Debian, Fedora, BSD, Gentoo, MacOS).

## Команды

| Команда | Пояснение |
|---------|----------|
| `ls` | Просмотр содержимого директории |
| `cd` | Смена текущей директории |
| `echo` | Вывод текста |
| `clear` | Очистка экрана |
| `wc` | Подсчет строк, слов и символов в файле |
| `touch` | Создание новых файлов |
| `chmod` | Изменение прав доступа |
| `vfs-save` | Сохранение состояния VFS |
| `exit` | Выход из эмулятора |

```
Создание директорий предусмотрено только через редактирование файлов различных VFS в формате JSON!
```

## Запуск

### Базовый запуск
```bash
python3 emulator.py
```

### С виртуальной файловой системой
```bash
python3 emulator.py --vfs deep_vfs.json
```

### Со стартовым скриптом
```bash
python3 emulator.py --script test_commands.txt
```

### Полная конфигурация
```bash
python3 emulator.py --vfs deep_vfs.json --script complete_test.txt
```

## Примеры использования

### Навигация по VFS
```bash
user@hostname:~$ ls
d level1/
d docs/
- root_file.txt (15 bytes)

user@hostname:~$ cd level1
user@hostname:level1$ ls
d level2/
d sibling_dir/
- level1_file.txt (12 bytes)

user@hostname:level1$ cd level2/level3
user@hostname:level1/level2/level3$ ls
- deep_file.txt (23 bytes)
- binary_data.bin (33 bytes)
```

### Создание и модификация файлов
```bash
user@hostname:~$ touch new_file.txt
touch: файл 'new_file.txt' создан

user@hostname:~$ chmod 755 new_file.txt
chmod: права на 'new_file.txt' изменены на 755

user@hostname:~$ wc root_file.txt
  1  3 15 root_file.txt
```

### Сохранение изменений
```bash
user@hostname:~$ vfs-save modified_system.json
VFS сохранена в modified_system.json
```

## Структура VFS

VFS хранится в JSON в след. формате:

```json
{
  "type": "directory",
  "children": {
    "file.txt": {
      "type": "file",
      "content": "SGVsbG8gV29ybGQ=",
      "permissions": "644"
    },
    "folder": {
      "type": "directory",
      "children": { ... }
    }
  }
}
```

## Тестирование

В проекте включены готовые тесты:

### Всё и сразу:
```bash
chmod +x run_all_vfs_tests.sh
./run_all_vfs_tests.sh
```

### Частично:
```bash
# Тест основных команд
./run_stage4_tests.sh

# Тест команд модификации
./run_stage5_tests.sh

# Демонстрация возможностей
chmod +x demo.sh
./demo.sh
```

## Файлы проекта

- `emulator.py` - основной файл эмулятора
- `*.json` - VFS-ки
- `*_test.txt` - тестовые скрипты
- `*.sh` - скрипты запуска тестов

## Особенности реализации

- Все операции с VFS выполняются в памяти
- Изменения сохраняются только при вызове `vfs-save`
- Парсер команд поддерживает кавычки и экранирование (shlex)
- Обработка ошибок подобна настоящим системам
- Имя пользователя генерируется на основе реальных данных ОС

## Протестировано на
Тестирование и написание программы выполнялись на MacOS 15.6.1 (24G90), вроде всё работало)
