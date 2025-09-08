#!/bin/bash

echo "=== Полное тестирование всех команд этапа 4 ==="
echo

echo "1. Тест основных команд:"
python3 emulator.py --vfs deep_vfs.json --script stage4_test.txt
echo

echo "2. Детальный тест echo:"
python3 emulator.py --script echo_test.txt
echo

echo "3. Детальный тест wc:"
python3 emulator.py --vfs deep_vfs.json --script wc_test.txt
echo

echo "4. Тест без VFS:"
python3 emulator.py --script stage4_no_vfs.txt
echo

echo "=== Все тесты этапа 4 завершены ==="