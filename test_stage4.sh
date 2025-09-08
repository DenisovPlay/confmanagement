#!/bin/bash

echo "=== Тест этапа 4: Основные команды ==="
python3 emulator.py --vfs deep_vfs.json --script stage4_test.txt
echo
echo "=== Тест завершен ==="