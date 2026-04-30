#!/bin/bash

if [ "$EUID" == 0 ]; then 
	continue;
	else echo "Нет, ты - ошибка!!!"
fi
