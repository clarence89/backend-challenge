# Back-End/Integration Challenge

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Requests

## Project Structure

``` bash
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

Database design

1. categories
2. products

Relationship

* categories.id → products.category_id

Each category contains 5 products.

Total records

5 categories
25 products

## Features Implemented

* CRUD endpoints for products
* SQL join returning product with category
* External API integration for currency conversion
* Summary endpoints
* total number of products
* number of products per category
* SQL schema and seed scripts

## Features Not Implemented

* Sentry for Project Monitoring
* `drf-yasg` or Swagger for API Documentation
* Cache for Currency Converter
* Mysql/PostgreSQL
* Containerization (Docker)
* Proper Security
* JWT Authentication
* Viewsets (CRUD Should just use Viewset but since the task needs SQL Scripts I just used an alternative)
* Models (Due to requirements)
* Migrations (Due to requirements)
* Middlewares (Overkill to implement)
* Row Locking to prevent Race Conditions
* Atomic Database

## Setup Instructions

### 1 Clone the repository

``` bash
git clone https://github.com/clarence89/backend-challenge.git
cd backend-challenge
```

### 2 Create Python virtual environment

``` bash
python -m venv venv
```

Activate environment

Mac Linux

``` bash
source venv/bin/activate
```

Windows

``` bash
venv\Scripts\activate
```

### 3 Install dependencies

``` bash
pip install -r requirements.txt
```

### 4 Initialize the database

Run the database initialization script which executes the SQL schema and seed data.

``` bash
python api/db_init.py
```

This creates the SQLite database and inserts the sample records.

### 5 Start the server

``` bash
python manage.py runserver
```

Server runs at

``` bash
http://127.0.0.1:8000
```

## API Endpoints

Get all products

``` bash
GET /api/products
```

Get product by id

``` bash
GET /api/products/<id>
```

Create product

``` bash
POST /api/products/create
```

Example body

``` bash
{
"name":"Tablet",
"price":300,
"stock":15,
"category_id":1
}
```

Update product

``` bash
PUT /api/products/<id>/update
```

Delete product

``` bash
DELETE /api/products/<id>/delete
```

Return products with category (SQL JOIN)

``` bash
GET /api/products-with-category
```

Convert product price using exchange rate API

``` bash
GET /api/products/<id>/convert?currency=EUR
```

## Summary Endpoints

Total number of products

``` bash
GET /api/summary/total-products
```

Number of products per category

``` bash
GET /api/summary/products-per-category
```

## Database Schema

Categories table

``` bash
id
name
is_active
created_at
```

Products table

``` bash
id
category_id
name
price
stock
created_at
```

Foreign key

``` bash
products.category_id → categories.id
```

## SQL Scripts

Schema creation

``` bash
sql/schema.sql
```

Seed data

``` bash
sql/seed.sql
```

The seed file inserts:

5 categories
5 products per category

## External API Integration

The endpoint

``` bash
GET /api/products/<id>/convert
```

calls the ExchangeRate API to convert the product price from USD to another currency.

Basic error handling included

invalid currency
external API failure
missing product

## Testing

You can test endpoints using

curl
Postman
browser for GET endpoints

Example

``` bash
http://127.0.0.1:8000/api/products
```
