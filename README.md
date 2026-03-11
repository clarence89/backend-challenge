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

1. categories
2. products

Relationship

* categories.id → products.category_id

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

Get all products (supports pagination & category filter):

```bash
GET /api/products?page=1&limit=10&category_id=1
```

Get product by id:

```bash
GET /api/products/<id>
```

Create product:

```bash
POST /api/products/create
```

Example body:

```json
{
  "name": "Tablet",
  "price": 300,
  "stock": 15,
  "category_id": 1
}
```

Update product:

```bash
PUT /api/products/<id>/update
```

Delete product (soft delete):

```bash
DELETE /api/products/<id>/delete
```

Return products with category (SQL JOIN):

```bash
GET /api/products-with-category
```

Convert product price using ExchangeRate API:

```bash
GET /api/products/<id>/convert?currency=EUR
```

### Categories

Get all categories (supports pagination & name search):

```bash
GET /api/categories?page=1&limit=10&search=Electronics
```

Get category by id:

```bash
GET /api/categories/<id>
```

Create category:

```bash
POST /api/categories/create
```

Example body:

```json
{
  "name": "Office"
}
```

Update category:

```bash
PUT /api/categories/<id>/update
```

Delete category (soft delete):

```bash
DELETE /api/categories/<id>/delete
```

### Summary Endpoints

Total number of products:

```bash
GET /api/summary/total-products
```

Number of products per category:

```bash
GET /api/summary/products-per-category
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
