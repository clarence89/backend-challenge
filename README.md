# Back-End/Integration Challenge

## Tech Stack

* Python 3.12
* Django
* Django REST Framework
* SQLite
* Requests

## Project Structure

```bash
inventory_backend_exam
│
├─ api
│  ├─ views.py
│  ├─ urls.py
│  └─ db_init.py
│
├─ backend
│  ├─ settings.py
│  └─ urls.py
│
├─ sql
│  ├─ schema.sql
│  └─ seed.sql
│
├─ requirements.txt
└─ README.md
```

## Database Design

1. `categories`
2. `products`

Relationship

* `categories.id → products.category_id`

Each category contains 5 products.

Total records:

* 5 categories
* 25 products

## Features Implemented

* CRUD endpoints for **products** and **categories**
* SQL join returning product with category
* Pagination and filtering for products and categories
* External API integration for currency conversion
* Summary endpoints:

  * Total number of products
  * Number of products per category
* SQL schema and seed scripts

## Features Not Implemented

* Sentry for Project Monitoring
* Swagger (`drf-yasg`) for API Documentation
* Cache for Currency Converter
* MySQL/PostgreSQL
* Containerization (Docker)
* JWT Authentication
* Django Models & Migrations (raw SQL required)
* Row Locking / Atomic Transactions (overkill for exam scope)

## Setup Instructions

### 1 Clone the repository

```bash
git clone https://github.com/clarence89/backend-challenge.git
cd backend-challenge
```

### 2 Create Python virtual environment

```bash
python -m venv venv
```

Activate environment:

**Mac / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3 Install dependencies

```bash
pip install -r requirements.txt
```

### 4 Initialize the database

```bash
python api/db_init.py
```

### 5 Start the server

```bash
python manage.py runserver
```

Server runs at:

```bash
http://127.0.0.1:8000
```

## API Endpoints

### Products

Get all products (pagination + category filter)

Endpoint

```bash
GET /api/products?page=1&limit=10&category_id=1
```

Curl example

```bash
curl "http://127.0.0.1:8000/api/products?page=1&limit=10&category_id=1"
```

Get product by id

Endpoint

```bash
GET /api/products/<id>
```

Curl example

```bash
curl http://127.0.0.1:8000/api/products/1
```

Create product

Endpoint

```bash
POST /api/products/create
```

Example body

```json
{
  "name": "Tablet",
  "price": 300,
  "stock": 15,
  "category_id": 1
}
```

Curl example

```bash
curl -X POST http://127.0.0.1:8000/api/products/create \
-H "Content-Type: application/json" \
-d '{"name":"Tablet","price":300,"stock":15,"category_id":1}'
```

Update product

Endpoint

```bash
PUT /api/products/<id>/update
```

Curl example

```bash
curl -X PUT http://127.0.0.1:8000/api/products/1/update \
-H "Content-Type: application/json" \
-d '{"name":"Tablet Pro","price":350,"stock":12}'
```

Delete product (soft delete)

Endpoint

```bash
DELETE /api/products/<id>/delete
```

Curl example

```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/delete
```

Return products with category (SQL JOIN)

Endpoint

```bash
GET /api/products-with-category
```

Curl example

```bash
curl http://127.0.0.1:8000/api/products-with-category
```

Convert product price using ExchangeRate API

Endpoint

```bash
GET /api/products/<id>/convert?currency=EUR
```

Curl example

```bash
curl "http://127.0.0.1:8000/api/products/1/convert?currency=EUR"
```

### Categories

Get all categories (pagination + search)

Endpoint

```bash
GET /api/categories?page=1&limit=10&search=Electronics
```

Curl example

```bash
curl "http://127.0.0.1:8000/api/categories?page=1&limit=10&search=Electronics"
```

Get category by id

Endpoint

```bash
GET /api/categories/<id>
```

Curl example

```bash
curl http://127.0.0.1:8000/api/categories/1
```

Create category

Endpoint

```bash
POST /api/categories/create
```

Example body

```json
{
  "name": "Office"
}
```

Curl example

```bash
curl -X POST http://127.0.0.1:8000/api/categories/create \
-H "Content-Type: application/json" \
-d '{"name":"Office"}'
```

Update category

Endpoint

```bash
PUT /api/categories/<id>/update
```

Curl example

```bash
curl -X PUT http://127.0.0.1:8000/api/categories/1/update \
-H "Content-Type: application/json" \
-d '{"name":"Office Equipment"}'
```

Delete category (soft delete)

Endpoint

```bash
DELETE /api/categories/<id>/delete
```

Curl example

```bash
curl -X DELETE http://127.0.0.1:8000/api/categories/1/delete
```

### Summary Endpoints

Total number of products

Endpoint

```bash
GET /api/summary/total-products
```

Curl example

```bash
curl http://127.0.0.1:8000/api/summary/total-products
```

Number of products per category

Endpoint

```bash
GET /api/summary/products-per-category
```

Curl example

```bash
curl http://127.0.0.1:8000/api/summary/products-per-category
```

## Database Schema

**Categories table**

| Column     | Type                               |
| ---------- | ---------------------------------- |
| id         | INTEGER PK                         |
| name       | TEXT NOT NULL                      |
| is_active  | BOOLEAN DEFAULT 1                  |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP |

**Products table**

| Column      | Type                               |
| ----------- | ---------------------------------- |
| id          | INTEGER PK                         |
| category_id | INTEGER FK → categories.id         |
| name        | TEXT NOT NULL                      |
| price       | DECIMAL(10,2) NOT NULL             |
| stock       | INTEGER NOT NULL                   |
| is_active   | BOOLEAN DEFAULT 1                  |
| created_at  | DATETIME DEFAULT CURRENT_TIMESTAMP |

Index:

```sql
CREATE INDEX idx_products_category ON products(category_id);
```

## SQL Scripts

Schema creation:

```bash
sql/schema.sql
```

Seed data:

```bash
sql/seed.sql
```

*5 categories + 5 products per category*

## External API Integration

**Endpoint:**

```bash
GET /api/products/<id>/convert
```

* Converts product price from USD to requested currency
* Basic error handling:

  * invalid currency
  * missing product
  * external API failure

## Testing

You can test endpoints using:

* curl
* Postman
* Browser (for GET endpoints)

Example:

```bash
http://127.0.0.1:8000/api/products
```
