#!/bin/bash

echo "=== Тест VFS с несколькими файлами ==="
python3 emulator.py --vfs multi_files_vfs.json --script multi_files_test.txt
echo