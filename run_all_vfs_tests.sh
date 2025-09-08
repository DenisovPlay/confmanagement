#!/bin/bash

echo "Начало теста эмулятора с VFS"
echo "====================================================="
echo

chmod +x test_no_params.sh
chmod +x test_with_script.sh  
chmod +x test_full_params.sh
chmod +x test_error_handling.sh
chmod +x test_minimal_vfs.sh
chmod +x test_multi_files_vfs.sh
chmod +x test_deep_vfs.sh

echo "1. Запуск теста без параметров..."
./test_no_params.sh

echo
echo "2. Запуск теста со стартовым скриптом..."
./test_with_script.sh

echo  
echo "3. Запуск теста с полными параметрами..."
./test_full_params.sh

echo
echo "4. Запуск теста обработки ошибок..."
./test_error_handling.sh

echo
echo "5. Запуск теста минимального VFS..."
./test_minimal_vfs.sh

echo
echo "6. Запуск теста VFS с несколькими файлами..."
./test_multi_files_vfs.sh

echo
echo "7. Запуск теста глубокого VFS..."
./test_deep_vfs.sh

echo
echo "8. Запуск полного теста всех команд..."
python3 emulator.py --vfs deep_vfs.json --script complete_test.txt

echo
echo "====================================================="
echo "Все тесты завершены"
echo "Созданные файлы:"
ls -la *.json | grep saved