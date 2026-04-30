#!/bin/bash

read -p "Введите ваш вес (в кг): " WEIGHT
read -p "Введите ваш рост (в метрах): " HEIGHT

echo "Вес: $WEIGHT"
echo "Рост: $HEIGHT"

BMI=$(echo "scale=2; $WEIGHT / ($HEIGHT * $HEIGHT)" | bc -l)

echo "Ваше значение индекса массы тела: $BMI"
