#!/bin/bash

FILE="./system.log"
ERROR_CODE=1

if [ -f "$FILE" ]; then
    echo "Лог-файл найден."
else
    echo "Ошибка: файл не существует."
fi

case $ERROR_CODE in
    0)
        echo "Статус: Ошибок нет." ;;
    1)
        echo "Статус: Критическая ошибка! Не трогайте ПК! Не дышите!" ;;
    *)
        echo "Статус: Неизвестный код." ;;
esac
