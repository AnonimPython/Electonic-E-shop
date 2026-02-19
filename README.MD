# ElectroNIC – Modern Django E-commerce

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/JWT-auth-orange)](https://jwt.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://docker.com)

**ElectroNIC** is a fully functional e-commerce platform built with Django and Django REST Framework. It provides both a traditional HTML interface and a robust JSON API with JWT authentication. The project includes user management (with balance), product catalog, shopping cart, order processing, and an admin panel – all containerized with Docker for easy deployment.

---

## Features

### User Management

* Registration & login (session-based for web, JWT for API)
* Personal profile with **balance** (can be topped up)
* Admin panel for user managementProducts
* Product catalog with name, description, price, stock
* Multiple product images (main + thumbnails)
* Public API endpoint: `GET /api/products/`
* Admin-only create/edit/delete (via admin panel or API with admin rights)

### Shopping Cart

* Add, remove, update quantity of items
* Cart is stored per user
* REST API endpoints for cart operations

### Orders

* Create order from current cart
* Automatic checks: stock availability, sufficient balance
* Deducts items from stock and user balance
* Clears cart after successful order
* Order history for authenticated users

### Authentication

* Session authentication for web interface
* **JWT authentication** for API (access + refresh tokens)
* Token obtain and refresh endpoints

### Docker

* PostgreSQL and Django services via docker-compose
* Environment variables support
* Ready for production deployment

---

## Tech Stack

* **Backend:** Django 4.2, Django REST Framework 3.14
* **Authentication:** Session + JWT (djangorestframework-simplejwt)
* **Database:** PostgreSQL 15 (SQLite for local dev)
* **Containerization:** Docker, Docker Compose
* **Frontend:** HTML5, CSS3
* **Container:** Doker

---

## Project Structure

**text**

```
electronic/
├── config/               # Django project settings (settings.py, urls.py)
├── users/                # User app (custom user model, balance)
├── products/             # Product catalog, images
├── cart/                 # Shopping cart models and logic
├── orders/               # Order processing
├── templates/            # HTML templates
├── static/               # CSS, images
├── .envs/                # Environment variables (not committed)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Quick Start

### Prerequisites

* Python 3.10+
* PostgreSQL (if running locally without Docker) or Docker
* Docker & Docker Compose (optional, but recommended)

### Local Development (without Docker)

1. **Clone the repository:**
   **bash**

   ```
   git clone https://github.com/yourusername/electronic.git
   cd electronic
   ```
2. **Create and activate virtual environment:**
   **bash**

   ```
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   .\venv\Scripts\activate       # Windows
   ```
3. **Install dependencies:**
   **bash**

   ```
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**

   * Open `.envs/.env`
   * Edit the file with your database credentials
5. **Run migrations:**
   **bash**

   ```
   python manage.py migrate
   ```
6. **Create a superuser:**
   **bash**

   ```
   python manage.py createsuperuser
   ```
7. **Start the development server:**
   **bash**

   ```
   python manage.py runserver
   ```
8. Visit `http://localhost:8000` – you should see the product catalog.

### Docker Deployment

1. **Ensure Docker and Docker Compose are installed.**
2. **Copy environment example:**
   **bash**

   ```
   cp .envs/.env
   ```

   Edit `.envs/.env` with your values (leave `POSTGRES_HOST=db` for Docker. On local PC I use `POSTGRES_HOST=localhost`).
3. **Build and start containers:**
   **bash**

   ```
   docker-compose up --build
   ```
4. Access the site at `http://localhost:8000`.
5. **Create a superuser inside the container** (optional):
   **bash**

   ```
   docker exec -it shop_web python manage.py createsuperuser
   ```

---

## Environment Variables

Create a `.envs/.env` file based on the example:

**ini**

```
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

# PostgreSQL
POSTGRES_DB=shop_db
POSTGRES_USER=shop_user
POSTGRES_PASSWORD=strong_password
POSTGRES_HOST=localhost        # use 'db' when running with Docker Compose
POSTGRES_PORT=5432
```

---

## API Documentation

All API endpoints are prefixed with `/api/`. Authentication is via **JWT Bearer token** (except public endpoints).

### Authentication Endpoints

| Method | Endpoint                | Description                        | Auth |
| ------ | ----------------------- | ---------------------------------- | ---- |
| POST   | `/api/token/`         | Obtain JWT access & refresh tokens | ❌   |
| POST   | `/api/token/refresh/` | Refresh access token               | ❌   |

### Users

| Method | Endpoint                 | Description                                     | Auth |
| ------ | ------------------------ | ----------------------------------------------- | ---- |
| POST   | `/api/users/register/` | Register a new user                             | ❌   |
| GET    | `/api/users/profile/`  | Get current user profile                        | ✅   |
| POST   | `/api/users/deposit/`  | Add funds to balance (body:`{"amount": 500}`) | ✅   |

### Products

| Method | Endpoint                  | Description                       | Auth |
| ------ | ------------------------- | --------------------------------- | ---- |
| GET    | `/api/products/`        | List all products                 | ❌   |
| GET    | `/api/products/<slug>/` | Retrieve a single product by slug | ❌   |

### Cart

| Method | Endpoint                        | Description                                              | Auth |
| ------ | ------------------------------- | -------------------------------------------------------- | ---- |
| GET    | `/api/cart/`                  | Get current user's cart                                  | ✅   |
| POST   | `/api/cart/add/`              | Add item (body:`{"product_id": 1, "quantity": 2}`)     | ✅   |
| POST   | `/api/cart/update/`           | Update quantity (body:`{"item_id": 1, "quantity": 3}`) | ✅   |
| DELETE | `/api/cart/remove/<item_id>/` | Remove item from cart                                    | ✅   |

### Orders

| Method | Endpoint                 | Description                        | Auth |
| ------ | ------------------------ | ---------------------------------- | ---- |
| POST   | `/api/orders/create/`  | Create order from current cart     | ✅   |
| GET    | `/api/orders/history/` | Get order history for current user | ✅   |

---

## Authentication Example

1. **Obtain token:**
   **bash**

   ```
   curl -X POST http://localhost:8000/api/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "john", "password": "secret"}'
   ```

   Response:
   **json**

   ```
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   ```
2. **Use the token in protected requests:**
   **bash**

   ```
   curl -X GET http://localhost:8000/api/users/profile/ \
        -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
   ```

---

## Testing the API

You can test the API using tools like [Postman](https://postman.com/), [Insomnia](https://insomnia.rest/), or simple `curl` commands.

1. **Public endpoints** (no token required):
   * `GET http://localhost:8000/api/products/`
2. **Create a user** via registration:
   * `POST http://localhost:8000/api/users/register/` with JSON body containing `username`, `password`, `password2`, `email`.
3. **Get token** and start testing protected endpoints.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://license/) file for details.

## [Русская документация](READMERU.MD)
