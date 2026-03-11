from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(["GET"])
def categories(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))
    search = request.GET.get("search")
    offset = (page - 1) * limit

    base_query = "SELECT id,name,is_active,created_at FROM categories WHERE is_active=1"
    params = []

    if search:
        base_query += " AND name LIKE %s"
        params.append(f"%{search}%")

    base_query += " ORDER BY id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with connection.cursor() as cursor:
        cursor.execute(base_query, params)
        rows = cursor.fetchall()

        count_query = "SELECT COUNT(*) FROM categories WHERE is_active=1"
        count_params = []
        if search:
            count_query += " AND name LIKE %s"
            count_params.append(f"%{search}%")
        cursor.execute(count_query, count_params)
        result = cursor.fetchone()
        total = result[0] if result else 0
    data = [
        {"id": r[0], "name": r[1], "is_active": bool(r[2]), "created_at": r[3]}
        for r in rows
    ]

    return Response({"page": page, "limit": limit, "total": total, "data": data})


@api_view(["GET"])
def category(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id,name,is_active,created_at FROM categories WHERE id=%s AND is_active=1",
            [id],
        )
        row = cursor.fetchone()

    if not row:
        return Response({"error": "category_not_found"}, status=404)

    return Response(
        {"id": row[0], "name": row[1], "is_active": bool(row[2]), "created_at": row[3]}
    )


@api_view(["POST"])
def create_category(request):
    data = request.data
    if "name" not in data:
        return Response({"error": "name_required"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO categories(name) VALUES(%s)", [data["name"]])

    return Response({"status": "created"})


@api_view(["PUT"])
def update_category(request, id):
    data = request.data
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE categories SET name=%s WHERE id=%s", [data.get("name"), id]
        )
    return Response({"status": "updated"})


@api_view(["DELETE"])
def delete_category(request, id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE categories SET is_active=0 WHERE id=%s", [id])
    return Response({"status": "deleted"})


@api_view(["GET"])
def products(request):

    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))
    category_id = request.GET.get("category_id")

    offset = (page - 1) * limit

    base_query = """
    SELECT id,name,price,stock,category_id
    FROM products    
    WHERE is_deleted=false
    """

    params = []

    if category_id:
        base_query += " AND category_id = %s"
        params.append(category_id)

    base_query += " ORDER BY id LIMIT %s OFFSET %s"

    params.extend([limit, offset])

    with connection.cursor() as cursor:
        cursor.execute(base_query, params)
        rows = cursor.fetchall()

    data = [
        {
            "id": r[0],
            "name": r[1],
            "price": float(r[2]),
            "stock": r[3],
            "category_id": r[4],
        }
        for r in rows
    ]

    return Response(data)


@api_view(["GET"])
def product(request, id):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id,name,price,stock,category_id,created_at
            FROM products
            WHERE id=%s AND is_deleted=false
            """,
            [id],
        )
        row = cursor.fetchone()

    if not row:
        return Response({"error": "product_not_found"}, status=404)

    return Response(
        {
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "stock": row[3],
            "category_id": row[4],
            "created_at": row[5],
        }
    )


@api_view(["POST"])
def create_product(request):

    data = request.data

    required = ["name", "price", "stock", "category_id"]

    for field in required:
        if field not in data:
            return Response({"error": f"{field}_required"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO products(category_id,name,price,stock)
            VALUES(%s,%s,%s,%s)
            """,
            [data["category_id"], data["name"], data["price"], data["stock"]],
        )

    return Response({"status": "created"})


@api_view(["PUT"])
def update_product(request, id):

    data = request.data

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE products
            SET name=%s,price=%s,stock=%s
            WHERE id=%s
            """,
            [data.get("name"), data.get("price"), data.get("stock"), id],
        )

    return Response({"status": "updated"})


@api_view(["DELETE"])
def delete_product(request, id):

    with connection.cursor() as cursor:
        cursor.execute("UPDATE products SET is_deleted=true WHERE id=%s", [id])

    return Response({"status": "deleted"})


@api_view(["GET"])
def products_with_category(request):

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.price,
            p.stock,
            c.name
        FROM products p
        JOIN categories c
        ON p.category_id = c.id
        ORDER BY p.id
        """)

        rows = cursor.fetchall()

    data = [
        {
            "id": r[0],
            "name": r[1],
            "price": float(r[2]),
            "stock": r[3],
            "category": r[4],
        }
        for r in rows
    ]

    return Response(data)


@api_view(["GET"])
def convert_price(request, id):
    # Best to us to Cache this if this is a real project with key to product id + currency
    currency = request.GET.get("currency", "EUR")

    with connection.cursor() as cursor:
        cursor.execute("SELECT name,price FROM products WHERE id=%s", [id])
        row = cursor.fetchone()

    if not row:
        return Response({"error": "product_not_found"}, status=404)

    try:

        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)

        data = r.json()

        rate = data["rates"].get(currency)

        if not rate:
            return Response({"error": "invalid_currency"}, status=400)

        converted = float(row[1]) * rate

        return Response(
            {
                "product": row[0],
                "usd_price": float(row[1]),
                "converted_price": round(converted, 2),
                "currency": currency,
            }
        )

    except requests.RequestException:
        return Response({"error": "external_api_failed"}, status=500)


@api_view(["GET"])
def total_products(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM products")
        result = cursor.fetchone()
        count = result[0] if result else 0

    return Response({"total_products": count})


@api_view(["GET"])
def products_per_category(request):

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
            c.name,
            COUNT(p.id)
        FROM categories c
        LEFT JOIN products p
        ON p.category_id = c.id
        GROUP BY c.name
        ORDER BY c.name
        """)

        rows = cursor.fetchall()

    data = [{"category": r[0], "product_count": r[1]} for r in rows]

    return Response(data)
