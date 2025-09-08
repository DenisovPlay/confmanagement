#!/bin/bash

echo "=== Тестирование этапа 5: Дополнительные команды ==="
echo

echo "1. Основной тест touch и chmod с VFS:"
python3 emulator.py --vfs deep_vfs.json --script stage5_test.txt
echo

echo "2. Тест без VFS:"
python3 emulator.py --script stage5_no_vfs_test.txt
echo

echo "3. Тест обработки ошибок:"
python3 emulator.py --vfs deep_vfs.json --script stage5_error_test.txt
echo

echo "=== Все тесты этапа 5 завершены ==="