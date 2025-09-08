#!/bin/bash

echo "Начало теста"
echo "================================================"
echo

chmod +x test_no_params.sh
chmod +x test_with_script.sh  
chmod +x test_full_params.sh

echo "Тест без параметров..."
./test_no_params.sh

echo
echo "Тест со стартовым скриптом..."
./test_with_script.sh

echo  
echo "Тест с полными параметрами..."
./test_full_params.sh

echo
echo "================================================"
echo "Всё"