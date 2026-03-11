INSERT INTO
    categories (name, is_active)
VALUES
    ('Electronics', 1),
    ('Books', 1),
    ('Clothing', 1),
    ('Home', 1),
    ('Sports', 1);

INSERT INTO
    products (category_id, name, price, stock)
VALUES

    (1, 'Laptop', 1200, 10),
    (1, 'Keyboard', 50, 30),
    (1, 'Mouse', 25, 50),
    (1, 'Monitor', 300, 12),
    (1, 'Headphones', 80, 25),

    (2, 'Python Programming', 40, 15),
    (2, 'Django Guide', 45, 10),
    (2, 'Data Science Handbook', 60, 8),
    (2, 'Clean Code', 55, 12),
    (2, 'Algorithms Book', 70, 7),

    (3, 'Jacket', 90, 8),
    (3, 'T-Shirt', 20, 50),
    (3, 'Jeans', 60, 20),
    (3, 'Sneakers', 110, 15),
    (3, 'Cap', 15, 40),

    (4, 'Coffee Maker', 70, 12),
    (4, 'Blender', 65, 10),
    (4, 'Vacuum Cleaner', 150, 6),
    (4, 'Microwave', 180, 9),
    (4, 'Air Fryer', 120, 11),

    (5, 'Basketball', 30, 20),
    (5, 'Football', 28, 18),
    (5, 'Tennis Racket', 95, 7),
    (5, 'Yoga Mat', 25, 30),
    (5, 'Dumbbells', 85, 14);