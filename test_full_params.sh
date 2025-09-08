#!/bin/bash

echo "=== Тест 3: Запуск эмулятора с VFS и стартовым скриптом ==="
mkdir -p test_vfs
python3 emulator.py --vfs ./test_vfs --script extended_test.txt
echo

echo "=== Тест завершен ==="