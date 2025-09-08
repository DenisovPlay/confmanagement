#!/bin/bash

echo "=== Демка эмулятора ==="
echo

echo "1. Тест без VFS:"
python3 emulator.py --script demo_no_vfs.txt
echo

echo "2. Тест с минимальным VFS:"
python3 emulator.py --vfs minimal_vfs.json --script demo_minimal.txt
echo

echo "3. Тест с глубоким VFS:"
python3 emulator.py --vfs deep_vfs.json --script demo_deep.txt
echo

echo "=== Демка завершена ==="