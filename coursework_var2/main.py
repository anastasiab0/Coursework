from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
import asyncpg
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
# Инициализация FastAPI и шаблонов
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Настройки подключения к БД
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'coursework'
# DB_HOST=os.getenv("DB_HOST", "postgres")
# DB_USER=os.getenv("DB_USER", "postgres")
# DB_PASSWORD=os.getenv("DB_PASSWORD", "postgres")
# DB_NAME=os.getenv("DB_NAME", "coursework")
# Параметры подключения к PostgreSQL
async def get_db_connection():
    return await asyncpg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Модели данных для валидации запросов с использованием Pydantic
class Planes(BaseModel):
    flight_num_planes: str
    type_la: Optional[str] = None
    bort_num: Optional[str] = None

class Flights(BaseModel):
    flight_num: str
    city_1: Optional[str] = None
    city_2: Optional[str] = None

app.mount("/static", StaticFiles(directory="static"), name='background')

# Главная страница с данными из базы
@app.get("/", response_class=HTMLResponse) # декорация для обработки GET запроса
async def main(request: Request): # Определяем асинхронную функцию main
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    planes= [] # Инициализируем пустой список для хранения данных о самолетах
    flights =[] # Инициализируем пустой список для хранения данных о рейсах
    await conn.close() # Закрываем соединение с базой данных
    return templates.TemplateResponse("mainpage.html", {"request": request, "planes": planes, "flights": flights})  # Возвращаем ответ в виде HTML-шаблона

# Маршруты для управления страницами
@app.get("/add_planes_page", response_class=HTMLResponse) # декорация для обработки GET запроса
async def add_planes_page(request: Request): # Определяем асинхронную функцию
    return templates.TemplateResponse("addplanes.html", {"request": request}) # Возвращаем ответ в виде HTML-шаблона

@app.get("/add_flights_page", response_class=HTMLResponse) # декорация для обработки GET запроса
async def add_flights_page(request: Request): # Определяем асинхронную функцию
    return templates.TemplateResponse("addflights.html", {"request": request}) # Возвращаем ответ в виде HTML-шаблона

# Функция для добавления ЛА 
@app.post("/add_planes") # Декорируем функцию для обработки POST-запросов
async def add_planes(
    request: Request,
    flight_num_planes: str = Form(...), # Обязательный параметр
    type_la: Optional[str] = Form(None), # Необязательный параметр
    bort_num: Optional[str] = Form(None) # Необязательный параметр
):
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        # Добавление нового ЛА
        await conn.execute(
            "INSERT INTO planes (flight_num_planes, type_la, bort_num) VALUES ($1, $2, $3)",
            flight_num_planes, type_la, bort_num
        )
    except Exception as e: # Обраьотка исключения (ошибки)
        message = f"Ошибка: {str(e)}" # Формируем сообщение об ошибке
        await conn.close() # Закрываем соединение с базой данных
        return templates.TemplateResponse("addplanes.html", {"request": request, "message": message}) # Возвращаем ответ с сообщением об ошибке
    finally:
        await conn.close() # Закрываем соединение с базой данных
        message = f"Plane {flight_num_planes} is successfully added!" # Формируем сообщение о корректной работе
        return templates.TemplateResponse("addplanes.html", {"request": request, "message": message}) # Возвращаем ответ с сообщением об успехе

# Функция для добавления рейса
@app.post("/add_flights") # Декорируем функцию для обработки POST-запросов
async def add_flights(
    request: Request,
    flight_num: str = Form(...), # Обязательный параметр
    city_1: Optional[str] = Form(None), # Необязательный параметр
    city_2: Optional[str] = Form(None) # Необязательный параметр
):
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        # Добавление нового рейса
        await conn.execute(
            "INSERT INTO flights (flight_num, city_1, city_2) VALUES ($1, $2, $3)",
            flight_num, city_1, city_2
        )
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        await conn.close()
        return templates.TemplateResponse("addflights.html", {"request": request, "message": message})
    finally:
        await conn.close()
        message = f"Flight {flight_num} is successfully added!"
        return templates.TemplateResponse("addflights.html", {"request": request, "message": message})
    #return RedirectResponse("/", status_code=303)

# Маршруты для управления страницами
# Удаление записи из таблицы ЛА
@app.get("/delete_planes/{flight_num_planes}", response_class=RedirectResponse) # Декорируем функцию для обработки GET-запросов
async def delete_planes(flight_num_planes: str): # Определяем асинхронную функцию
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        # Удаляем ЛА по номеру рейса
        await conn.execute("DELETE FROM planes WHERE flight_num_planes = $1", flight_num_planes) # SQL-запрос для удаления записи
    except Exception as e:
        print(f"Ошибка при удалении ЛА: {str(e)}")
    finally:
        await conn.close() # Закрываем соединение с базой данных
    return RedirectResponse("/", status_code=303) # Перенаправляем пользователя на главную страницу

# Удаление записи из таблицы рейсов
@app.get("/delete_flights/{flight_num}", response_class=RedirectResponse) # Декорируем функцию для обработки GET-запросов
async def delete_flights(flight_num: str): # Определяем асинхронную функцию
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        # Удаляем рейс по номеру рейса
        await conn.execute("DELETE FROM flights WHERE flight_num = $1", flight_num) # SQL-запрос для удаления записи
    except Exception as e:
        print(f"Ошибка при удалении рейса: {str(e)}")
    finally:
        await conn.close() # Закрываем соединение с базой данных
    return RedirectResponse("/", status_code=303) # Перенаправляем пользователя на главную страницу

# Удаление атрибутов из таблицы ЛА
@app.post("/delete_planes_attribute")
async def delete_planes_attribute(
    request: Request,
    flight_num_planes: str = Form(...), # Обязательный параметр формы
    attribute_name: str = Form(...), # Обязательный параметр формы
):
    conn = await get_db_connection()
    try:
        # Удаляем атрибут ЛА
        await conn.execute(f"UPDATE planes SET {attribute_name} = NULL WHERE flight_num_planes = $1", flight_num_planes) # SQL-запрос для обновления записи
    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        await conn.close()

    return RedirectResponse("/", status_code=303) # Перенаправляем пользователя на главную страницу

# Удаление атрибутов из таблицы рейсов
@app.post("/delete_flights_attribute")
async def delete_flights_attribute(
    request: Request,
    flight_num: str = Form(...), # Обязательный параметр формы
    attribute_name: str = Form(...), # Обязательный параметр формы
):
    conn = await get_db_connection()
    try:
        # Удаляем атрибут рейса
        await conn.execute(f"UPDATE flights SET {attribute_name} = NULL WHERE flight_num = $1", flight_num) # SQL-запрос для обновления записи
    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        await conn.close()

    return RedirectResponse("/", status_code=303) # Перенаправляем пользователя на главную страницу

# Новый маршрут для поиска
@app.get("/search", response_class=HTMLResponse) # Декорируем функцию для обработки GET-запросов
async def search(request: Request, search_value: str, attribute: str):  # Определяем асинхронную функцию
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        if attribute == "flight_num_planes" or attribute =="flight_num": # если искомое поле номер рейса
            query = "SELECT * FROM planes, flights WHERE (planes.flight_num_planes ILIKE $1 AND flights.flight_num ILIKE $1)" # SQL-запрос для поиска по номеру рейса в обеих таблицах
            results = await conn.fetch(query, f"%{search_value}%") # Выполняем запрос, передавая значение для поиска с учетом подстановочных знаков
            return templates.TemplateResponse("mainpage.html", {"request": request, "planes": results, "flights": results}) # Возвращаем ответ в виде HTML-шаблона
        elif attribute == "type_la": # если искомое поле тип ЛА
            query = "SELECT * FROM planes WHERE type_la ILIKE $1" # SQL-запрос для поиска по типу самолета
            results = await conn.fetch(query, f"%{search_value}%")
            return templates.TemplateResponse("mainpage.html", {"request": request, "planes": results, "flights": []})
        elif attribute == "bort_num": # если искомое поле бортовой номер
            query = "SELECT * FROM planes WHERE bort_num ILIKE $1" # SQL-запрос для поиска по бортовому номеру  
            results = await conn.fetch(query, f"%{search_value}%")
            return templates.TemplateResponse("mainpage.html", {"request": request, "planes": results, "flights": []})
        elif attribute == "city_1": # если искомое поле город отправления
            query = "SELECT * FROM flights WHERE city_1 ILIKE $1" # SQL-запрос для поиска по городу отправления 
            results = await conn.fetch(query, f"%{search_value}%")
            return templates.TemplateResponse("mainpage.html", {"request": request, "planes": [], "flights": results})
        elif attribute == "city_2": # если искомое поле город прибытия
            query = "SELECT * FROM flights WHERE city_2 ILIKE $1" # SQL-запрос для поиска по городу прибытия 
            results = await conn.fetch(query, f"%{search_value}%")
            return templates.TemplateResponse("mainpage.html", {"request": request, "planes": [], "flights": results})
        else:
            query = "" # Если ни одно из условий не выполнено, присваиваем пустое значение запросу
    except Exception as e:
        results = [] # Присваиваем пустой список переменной results
    finally:
        await conn.close() # Закрываем соединение с базой данных

    # Передаем данные на шаблон
    return templates.TemplateResponse("mainpage.html", {"request": request, "planes": results, "flights": results})

@app.get("/view_db", response_class=HTMLResponse)  # Декорируем функцию для обработки GET-запросов
async def view_db(request: Request): # Определяем асинхронную функцию
    conn = await get_db_connection() # Устанавливаем соединение с базой данных
    try:
        # SQL-запрос для получения связанных данных
        # SQL-запрос для получения данных из таблиц 'planes' и 'flights'
        query = """
        SELECT COALESCE(p.flight_num_planes, f.flight_num) AS flight_num,
            p.type_la,
            p.bort_num,
            f.city_1,
            f.city_2
        FROM planes p
        FULL OUTER JOIN flights f
        ON p.flight_num_planes = f.flight_num;
        """
        # Выполнение запроса
        data = await conn.fetch(query) # Выполняем SQL-запрос и сохраняем результат в переменной 'data'
    except Exception as e:
        print(f"Ошибка при получении данных: {str(e)}")
        data = [] # Если произошла ошибка, инициализируем 'data' пустым списком
    finally:
        await conn.close() # Закрываем соединение с базой данных

    # Передаем данные на шаблон
    return templates.TemplateResponse("view_db.html", {"request": request, "data": data}) # Возвращаем ответ в виде HTML-шаблона 'view_db.html', передавая туда данные

# Запуск приложения
if __name__ == "__main__": # Проверяем, запущен ли скрипт напрямую
    import uvicorn # Импортируем библиотеку uvicorn для запуска сервера
    uvicorn.run(app, host="0.0.0.0", port=8088)  # Запускаем сервер на адресе '0.0.0.0' и порт 8088
#uvicorn main:app --port 8088