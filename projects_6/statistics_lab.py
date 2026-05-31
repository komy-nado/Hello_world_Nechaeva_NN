import psycopg2
import pandas as pd

# Так, ну поехали
# Ниже подключение к PostgreSQL

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="example"
)
print("Соединение успешно!")
cursor = conn.cursor()

# Склеиваю таблицы

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    price_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    price NUMERIC
)
""")
conn.commit()

# Добавляю тестовые данные

cursor.execute("""
INSERT INTO products (product_name, category)
VALUES
('Ноут', 'Электроника'),
('Звонилка', 'Электроника'),
('Дас ист стол (на нем сидят)', 'Мебель'),
('Это стул (за ним едят)', 'Мебель'),
('Маршалы', 'Аксессуары')
""")
cursor.execute("""
INSERT INTO prices (product_id, price)
VALUES
(1, 75000),
(1, 82000),
(2, 45000),
(2, 47000),
(3, 12000),
(3, 15000),
(4, 5000),
(4, 6500),
(5, 3000),
(5, 4500)
""")

conn.commit()

# Туть SQL JOIN и загрузка в DataFrame

query = """
SELECT
    p.product_name,
    p.category,
    pr.price
FROM prices pr
JOIN products p
    ON pr.product_id = p.product_id
"""
df = pd.read_sql(query, conn)
print("\nТаблица хоба:")
print(df)

# 5. Смотрю основыные статистики

mean_price = df["price"].mean()
median_price = df["price"].median()
std_price = df["price"].std()
min_price = df["price"].min()
max_price = df["price"].max()
print("\nСтатистику по ценам нате ((с.) Маяковский):")
print(f"Средняя цена: {mean_price:.2f} руб.")
print(f"Медиана: {median_price:.2f} руб.")
print(f"Стандартное отклонение: {std_price:.2f} руб.")
print(f"Минимальная цена: {min_price:.2f} руб.")
print(f"Максимальная цена: {max_price:.2f} руб.")

# Эт квартили и IQR 

Q1 = df["price"].quantile(0.25)
Q2 = df["price"].quantile(0.50)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1
print("\nКвартили, прости господи:")
print(f"Q1 = {Q1:.2f}")
print(f"Q2 = {Q2:.2f}")
print(f"Q3 = {Q3:.2f}")
print(f"IQR = {IQR:.2f}")

# Тут щас будут товары дороже Q3

expensive_products = df[df["price"] > Q3]
print("\nТра-та-та-товары с ценой выше Q3:")
print(
    expensive_products[
        ["product_name", "category", "price"]
    ]
)

# 7. Разделяю по категориям

grouped = (
    df.groupby("category")["price"]
    .agg(["count", "mean", "median", "std"])
    .sort_values(by="mean", ascending=False)
)
print("\nИ статистика по категориям:")
print(grouped)

# 8. Смотрю разлет цен

spread = (
    df.groupby("product_name")["price"]
    .agg(["min", "max"])
)

spread["difference"] = spread["max"] - spread["min"]
top5 = spread.sort_values(
    by="difference",
    ascending=False
).head(5)
print("\nТоп-5 (дай пять) тра-та-та-та-та с наибольшим разбросом цен:")
print(top5)

# 9. Так, ну тут тип отключаюсть. Кто бы пристрелил

conn.close()
print("\nСоединение все. Устало, ушло")