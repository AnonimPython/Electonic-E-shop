
# ElectroNIC – Современный интернет-магазин на Django

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/JWT-auth-orange)](https://jwt.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://docker.com)

**ElectroNIC** — это полнофункциональная платформа электронной коммерции, построенная на Django и Django REST Framework. Она предоставляет как традиционный HTML-интерфейс, так и мощный JSON API с JWT-аутентификацией. Проект включает управление пользователями (с балансом), каталог товаров, корзину, обработку заказов и панель администратора — всё упаковано в Docker для лёгкого развёртывания.

---

## Возможности

### Управление пользователями

- Регистрация и вход (сессии для веба, JWT для API)
- Личный профиль с **балансом** (возможность пополнения)
- Панель администратора для управления пользователями

### Товары

- Каталог товаров: название, описание, цена, остаток
- Несколько изображений для каждого товара (главное + миниатюры)
- Публичный API: `GET /api/products/`
- Только администратор может создавать/редактировать/удалять товары (через админку или API)

### Корзина

- Добавление, удаление, изменение количества товаров
- Корзина привязана к пользователю
- REST API для работы с корзиной

### Заказы

- Создание заказа из текущей корзины
- Автоматическая проверка наличия товаров и достаточности баланса
- Списание товаров со склада и уменьшение баланса пользователя
- Очистка корзины после успешного заказа
- История заказов для аутентифицированных пользователей

### Аутентификация

- Сессионная аутентификация для веб-интерфейса
- **JWT-аутентификация** для API (access + refresh токены)
- Эндпоинты для получения и обновления токенов

### Docker

- Сервисы PostgreSQL и Django через docker-compose
- Поддержка переменных окружения
- Готовность к продакшену

---

## Технологический стек

- **Бэкенд:** Django 4.2, Django REST Framework 3.14
- **Аутентификация:** Сессии + JWT (djangorestframework-simplejwt)
- **База данных:** PostgreSQL 15 (или SQLite для локальной разработки)
- **Контейнеризация:** Docker, Docker Compose
- **Фронтенд:** HTML5, CSS3

---

## Структура проекта

electronic/
├── config/ # Django project settings (settings.py, urls.py)
├── users/ # User app (custom user model, balance)
├── products/ # Product catalog, images
├── cart/ # Shopping cart models and logic
├── orders/ # Order processing
├── templates/ # HTML templates
├── static/ # CSS, images
├── .envs/ # Environment variables (not committed)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

---

## Быстрый старт

### Предварительные требования

- Python 3.10+
- PostgreSQL (при локальном запуске без Docker) или Docker
- Docker & Docker Compose (опционально, но рекомендуется)

### Локальная разработка (без Docker)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/electronic.git
   cd electronic

2. **Создайте и активируйте виртуальное окружение:**
   **bash**

   ```
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   .\venv\Scripts\activate       # Windows
   ```
3. **Установите зависимости:**
   **bash**

   ```
   pip install -r requirements.txt
   ```
4. **Настройте переменные окружения:**

   * Откройте `.envs/.env`
   * Отредактируйте файл с вашими данными для подключения к БД
5. **Выполните миграции:**
   **bash**

   ```
   python manage.py migrate
   ```
6. **Создайте суперпользователя:**
   **bash**

   ```
   python manage.py createsuperuser
   ```
7. **Запустите сервер разработки:**
   **bash**

   ```
   python manage.py runserver
   ```
8. Откройте `http://localhost:8000` – вы увидите каталог товаров.

### Развёртывание через Docker

1. **Убедитесь, что Docker и Docker Compose установлены.**
2. **Скопируйте пример файла с переменными окружения:**
   **bash**

   ```
   cp .envs/.env .envs/.env
   ```

   Отредактируйте `.envs/.env` под свои нужды (для Docker укажите `POSTGRES_HOST=db`, для локального ПК используйте `POSTGRES_HOST=localhost`).
3. **Соберите и запустите контейнеры:**
   **bash**

   ```
   docker-compose up --build
   ```
4. Откройте сайт по адресу `http://localhost:8000`.
5. **Создайте суперпользователя внутри контейнера** (необязательно):
   **bash**

   ```
   docker exec -it shop_web python manage.py createsuperuser
   ```

---

## Переменные окружения

Создайте файл `.envs/.env` на основе примера:

**ini**

```
# Django
DJANGO_SECRET_KEY="your-secret-key-here"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

# PostgreSQL
POSTGRES_DB=shop_db
POSTGRES_USER=shop_user
POSTGRES_PASSWORD=strong_password
POSTGRES_HOST=localhost        # используйте 'db' при запуске с Docker Compose
POSTGRES_PORT=5432
```

---

## Документация API

Все API-эндпоинты имеют префикс `/api/`. Аутентификация осуществляется через **JWT Bearer токен** (кроме публичных эндпоинтов).

### Эндпоинты аутентификации

| Метод | Эндпоинт        | Описание                                    | Требуется аутентификация |
| ---------- | ----------------------- | --------------------------------------------------- | ----------------------------------------------- |
| POST       | `/api/token/`         | Получить JWT access и refresh токены | ❌                                              |
| POST       | `/api/token/refresh/` | Обновить access токен                  | ❌                                              |

### Пользователи

| Метод | Эндпоинт         | Описание                                                          | Требуется аутентификация |
| ---------- | ------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------- |
| POST       | `/api/users/register/` | Зарегистрировать нового пользователя    | ❌                                              |
| GET        | `/api/users/profile/`  | Получить профиль текущего пользователя | ✅                                              |
| POST       | `/api/users/deposit/`  | Пополнить баланс (тело:`{"amount": 500}`)            | ✅                                              |

### Товары

| Метод | Эндпоинт          | Описание                               | Требуется аутентификация |
| ---------- | ------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| GET        | `/api/products/`        | Список всех товаров           | ❌                                              |
| GET        | `/api/products/<slug>/` | Получить один товар по slug | ❌                                              |

### Корзина

| Метод | Эндпоинт                | Описание                                                                   | Требуется аутентификация |
| ---------- | ------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------- |
| GET        | `/api/cart/`                  | Получить корзину текущего пользователя          | ✅                                              |
| POST       | `/api/cart/add/`              | Добавить товар (тело:`{"product_id": 1, "quantity": 2}`)        | ✅                                              |
| POST       | `/api/cart/update/`           | Изменить количество (тело:`{"item_id": 1, "quantity": 3}`) | ✅                                              |
| DELETE     | `/api/cart/remove/<item_id>/` | Удалить товар из корзины                                      | ✅                                              |

### Заказы

| Метод | Эндпоинт         | Описание                                                        | Требуется аутентификация |
| ---------- | ------------------------ | ----------------------------------------------------------------------- | ----------------------------------------------- |
| POST       | `/api/orders/create/`  | Создать заказ из текущей корзины            | ✅                                              |
| GET        | `/api/orders/history/` | История заказов текущего пользователя | ✅                                              |

---

## Пример аутентификации

1. **Получить токен:**
   **bash**

   ```
   curl -X POST http://localhost:8000/api/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "john", "password": "secret"}'
   ```

   Ответ:
   **json**

   ```
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   ```
2. **Использовать токен в защищённых запросах:**
   **bash**

   ```
   curl -X GET http://localhost:8000/api/users/profile/ \
        -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
   ```

---

## Тестирование API

Вы можете тестировать API с помощью инструментов вроде [Postman](https://postman.com/), [Insomnia](https://insomnia.rest/) или простых `curl`-команд.

1. **Публичные эндпоинты** (токен не требуется):
   * `GET http://localhost:8000/api/products/`
2. **Создайте пользователя** через регистрацию:
   * `POST http://localhost:8000/api/users/register/` с JSON-телом, содержащим `username`, `password`, `password2`, `email`.
3. **Получите токен** и начинайте тестировать защищённые эндпоинты.

---

## Вклад в проект

Приветствуются любые улучшения! Смело открывайте issues или отправляйте pull requests.

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](https://license/).
