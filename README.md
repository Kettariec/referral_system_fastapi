# API для реферальной системы

## Описание

Данный проект представляет собой RESTful API для реализации реферальной системы, разработанной с использованием **FastAPI**. API включает функции регистрации пользователей, управления реферальными кодами, а также работы с реферальными данными.

## Основные функциональные возможности

### Пользователи

- **Регистрация и аутентификация:**
  - Поддержка JWT-токенов для защиты эндпоинтов.
  - Верификация email-адреса при регистрации.

- **Управление реферальными кодами:**
  - Создание реферального кода с указанием срока действия.
  - Удаление реферального кода (одновременно может быть только один код пользователя).

### Реферальная система

- **Получение реферального кода по email-адресу реферера.**
- **Регистрация нового пользователя с использованием реферального кода.**
- **Получение информации о рефералах для реферера.**

### Дополнительные (опциональные) возможности

- **Кеширование:**
  - Хранение реферальных кодов в in-memory базе данных для повышения производительности.

## Технический стек

- **Backend:** FastAPI
- **База данных:** PostgreSQL
- **Асинхронные операции:** Полностью асинхронный ввод/вывод для всех операций (I/O bound).
- **Кеширование:** Redis (для in-memory хранения).

## Установка и запуск

### 1. Клонирование репозитория:

git clone https://github.com/Kettariec/referral_system_fastapi

### 2. Создание виртуального окружения:

pip install poetry
<br>poetry install
<br>poetry shell

### 3. Создание БД и настройка переменных окружения: 

Создайте базу данных PostgreSQL и файл .env в корне проекта. Укажите следующие переменные:

DB_USER=*имя пользователя базы данных*
<br>DB_PASS=*пароль базы данных*
<br>DB_NAME=*имя базы данных*
<br>SECRET_KEY=*секретный ключ*
<br>DB_HOST=localhost
<br>DB_PORT=5432
<br>ALGORITHM=HS256
<br>SMTP_HOST=smtp.gmail.com
<br>SMTP_PORT=465
<br>SMTP_USER=kettariec@gmail.com
<br>SMTP_PASS=zxnp oefx ulxl jmcj
<br>FRONTEND_URL=http://127.0.0.1:8000

### 4. Применение миграций:

alembic revision --autogenerate -m "Initial migration" 
alembic upgrade head

### 5. Запуск приложения:

uvicorn app.main:app --reload

### 6. Документация

После запуска API документация доступна по адресу:

    http://127.0.0.1:8000/docs