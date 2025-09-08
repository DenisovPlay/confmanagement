#!/bin/bash

echo "=== Тест 1: Запуск эмулятора без параметров ==="
python3 emulator.py &
EMULATOR_PID=$!
sleep 2
echo -e "ls\nexit" | python3 emulator.py
echo

echo "=== Тест завершен ==="