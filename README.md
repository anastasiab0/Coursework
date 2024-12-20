# Coursework
Курсовая работа 2 вариант Боровик Анастасия
Разархивировать файл
Необходимо наличие docker.desktop на запускаемой машине.
Открыть папку с проектом с VS Code.
В терминале прописать команду docker-compose up --build (docker.desktop должен быть запущен).
Дождаться окончания сборки контейнеров.
Перейти в docker.desktop во вкладку Containers. Найти группу контейнеров с наименованием папки с проектом, открыть ее, перейти по ссылке в браузер, нажав на нее в контейнере application.
Произвести работу с веб приложением.
По окончании работы, в docker.desktop нажать кнопку остановки работы контейнеров, либо в терминале VScode набрать ctrl+c.
Для удаления контейнеров в терминале VScode прописать команду docker-compose down -v, либо удалить группу контейнеров из docker.desktop, нажав на значок корзины.
Для контроля правильности отображения данных в веб приложении, необходимо в docker.desktop перейти по ссылке контейнера pgadmin в браузер.
Пройти регистрацию: логин: admin@admin.com пароль: admin
ПКМ на Sersers, Register, Server..
В поле Name во вкладке General ввести любое имя
Во вкладке Connection заполнить следующие поля: Host name/addres: postgres Port: 5432 Maintenance database: postgres Username: postgres Password: postgres
Нажать кнопку Save.
Контролировать наличие таблиц flights и planes во вкладке "зарегистрированное вами имя сервера" -> Databases -> coursework -> Schemas -> Tables.
