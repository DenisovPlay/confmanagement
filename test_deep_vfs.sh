#!/bin/bash

echo "=== Тест глубокого VFS ==="
python3 emulator.py --vfs deep_vfs.json --script test_script.sh
echo