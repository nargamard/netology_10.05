#!/usr/bin/env python3

#функции для множественной замены. Они помогут сделать красивый вывод.
def multiple_replace(target_str, replace_values):
    for i, j in replace_values.items():
        target_str = target_str.replace(i, j)
    return target_str

def multiple_clear(target_str, clear_values):
    for i, j in clear_values.items():
        target_str = target_str.replace(i, j)
    return target_str

import os
import sentry_sdk
sentry_sdk.init(
    dsn="https://8178be3e16584996b7cecfa0d007b448@o1320577.ingest.sentry.io/6576815",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

#Вариант, если хотим, чтобы скрипт отрабатывал в текущей директории
#bash_command = ["cd " + os.getcwd(), "git status"]

#Вариант, чтобы скрипт брал пути из конфигурационного файла

print ("\nЧтение списка репозиториев для проверки из 4.2.py.conf...")

#как вариант можно было использовать os.access("4.2.py.conf", os.R_OK)
try:
    pathlist = open("4.2.py.conf", "r")
    pathlist.close()
except IOError:
    print("Нет файла 4.2.py.conf, содержащего пути к репозиториям. Файл должен находиться в той же директории, что и этот скрипт")
    exit()

with open("4.2.py.conf", "r") as pathlist:
    paths = pathlist.read().splitlines()

division_by_zero = 1 / 0

#perem = func()

#Словарик для замены
replace_values = {"modified:   ": "Изменён: ", "new file:   ": "Добавлен: "}
#Словарик для очистки
clear_values = {"modified:   ": "", "new file:   ": ""}

for path in paths:
    #Сюда будем пихать уже использованные имена файлов. В цикле, потому что в разных репозиториях могут быть файлы с одинаковым именем.
    filelist = []

    print ("\nПуть к репозиторию: " + path)
    bash_command = ["cd " + path, "git status"]
    result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False

    for result in result_os.rsplit('\n'):
         if result.find('modified') != -1 or result.find('new') != -1:
            prepare_result = multiple_replace(result, replace_values)
            filename = multiple_replace(result, clear_values)
            if filename in filelist:
               break
            else:
               filelist.append(filename)
               print(prepare_result)
pathlist.close()

