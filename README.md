# Architecture-and-patterns
Для запуска сервера необходимо открыть терминал Linux(Ubuntu) в папке проекта и ввести:

gunicorn main:application

uwsgi --http :8000 --wsgi-file main.py

После этого открываем браузер и переходим по адресу: 127.0.0.1:8000

Попадаем на главную страницу index.html


Можно также прейти на другие странички проекта:
http://127.0.0.1:8000/products/

http://127.0.0.1:8000/contacts/