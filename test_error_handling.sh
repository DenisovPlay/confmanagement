#!/bin/bash

echo "=== Тест 4: Проверка остановки при ошибке ==="
python3 emulator.py --script error_test.txt
echo

echo "=== Тест завершен ==="