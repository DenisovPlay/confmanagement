#!/bin/bash

echo "=== Тест минимального VFS ==="
python3 emulator.py --vfs minimal_vfs.json --script minimal_test.txt
echo