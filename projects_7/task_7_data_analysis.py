
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

# шрифт))
plt.rcParams["font.family"] = "Comic Sans MS"

# тут подключаю бд
try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="postgres",
        database="postgres"
    )

    print("✓ Подключение установлено")

    cursor = connection.cursor()

    # создаю таблицы

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100),
        category VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(product_id),
        price NUMERIC
    )
    """)

    connection.commit()

    # очищаю таблицы

    cursor.execute(
        "TRUNCATE TABLE sales RESTART IDENTITY CASCADE"
    )

    cursor.execute(
        "TRUNCATE TABLE products RESTART IDENTITY CASCADE"
    )

    connection.commit()

    # добавляю данные

    cursor.execute("""
    INSERT INTO products (product_name, category)
    VALUES
    ('Ноут', 'Электроника'),
    ('Звонилка', 'Электроника'),
    ('Дас ист стол', 'Мебель'),
    ('Это стул (за ним едят)', 'Мебель'),
    ('Маршалы', 'Аксессуары')
    """)

    cursor.execute("""
    INSERT INTO sales (product_id, price)
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

    connection.commit()

    # SQL1 (средняя цена и количество продаж)

    df_products = pd.read_sql("""
        SELECT
            p.product_name AS product,
            p.category,
            ROUND(AVG(s.price)::numeric, 2) AS avg_price,
            COUNT(s.sale_id) AS total_sales
        FROM sales s
        JOIN products p
            ON s.product_id = p.product_id
        GROUP BY p.product_name, p.category
        ORDER BY avg_price DESC
    """, connection)

    # SQL2 (количество товаров по категориям)

    df_categories = pd.read_sql("""
        SELECT
            category,
            COUNT(product_id) AS products_count
        FROM products
        GROUP BY category
        ORDER BY products_count DESC
    """, connection)

    # SQL3 (все цены)

    df_all = pd.read_sql("""
        SELECT price
        FROM sales
    """, connection)

    # SQL4 товары-аномалии

    df_expensive = pd.read_sql("""
        SELECT
            p.product_name,
            p.category,
            s.price
        FROM sales s
        JOIN products p
            ON s.product_id = p.product_id
        WHERE s.price > (
            SELECT percentile_cont(0.75)
            WITHIN GROUP (ORDER BY price)
            FROM sales
        )
    """, connection)

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    if connection:
     connection.close()
     print("✓ Соединение закрыто")

# готовлю данные

overall_avg = df_products["avg_price"].mean()

median_price = df_all["price"].median()
std_price = df_all["price"].std()
mode_price = df_all["price"].mode()[0]

PRICE_THRESHOLD = 47000

bar_colors = [
    "#B85C42" if p > PRICE_THRESHOLD else "#A5D152"
    for p in df_products["avg_price"]
]

pie_labels = [
    f"{row.category} ({row.products_count} шт.)"
    for _, row in df_categories.iterrows()
]

# фигурку рисую.

fig = plt.figure(figsize=(16, 10))

fig.patch.set_facecolor("#dfe6d5")

fig.suptitle(
    "Анализ базы данных продаж",
    fontsize=16,
    fontweight="bold",
    color="#343B29"
)

gs = gridspec.GridSpec(
    2,
    3,
    figure=fig,
    width_ratios=[2, 1, 2],
    height_ratios=[5, 4],
    wspace=0.35,
    hspace=0.45
)

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1:3])

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor("#f6f3ea")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.3, color="#A39AA6")
    ax.set_axisbelow(True)

# график со средними ценами

bars1 = ax1.barh(
    df_products["product"],
    df_products["avg_price"],
    color=bar_colors,
    edgecolor="#f1eedf",
    height=0.6
)

for bar, value in zip(bars1, df_products["avg_price"]):
    ax1.text(
        bar.get_width() + 500,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.0f}",
        va="center",
        fontsize=9,
        color="#343B29"
    )

ax1.axvline(
    overall_avg,
    color="#642424",
    linestyle="--",
    linewidth=1.5,
    label=f"Среднее по больнице: {overall_avg:.0f}"
)

legend_patches = [
    Patch(facecolor="#A5D152", label="Норм ценник"),
    Patch(facecolor="#B85C42", label="Дюже дорого-богато")
]

ax1.legend(handles=legend_patches, fontsize=8)

ax1.set_xlabel("Средняя цена")

ax1.set_title(
    "Средняя цена товаров",
    fontweight="bold",
    color="#343B29"
    
)

# график с количеством продаж

bars2 = ax2.bar(
    df_products["product"],
    df_products["total_sales"],
    color="#9FB2CD",
    edgecolor="#f1eedf",
    width=0.6
)

for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        str(int(bar.get_height())),
        ha="center",
        fontsize=9,
        color="#343B29"
    )

ax2.set_ylabel("Количество продаж")

ax2.set_title(
    "Количество продаж товаров",
    fontweight="bold",
    color="#343B29"
)

ax2.set_xticks(range(len(df_products)))

ax2.set_xticklabels(
    df_products["product"],
    rotation=40,
    ha="right",
    fontsize=8
)

# диаграмочка

pie_colors = ["#7E2932", "#4B384C", "#986B6B"]

wedges, texts, autotexts = ax3.pie(
    df_categories["products_count"],
    labels=None,
    autopct="%1.0f%%",
    startangle=90,
    colors=pie_colors,
    wedgeprops={
        "edgecolor": "#f1eedf",
        "linewidth": 1.5
    }
)

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax3.legend(
    wedges,
    pie_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.25),
    fontsize=8,
    frameon=False
)

ax3.set_title(
    "Товары по категориям",
    fontweight="bold",
    color="#343B29"
)

# график распределения ценочек

price_counts = df_all["price"].value_counts().sort_index()

bars4 = ax4.bar(
    price_counts.index.astype(str),
    price_counts.values,
    color="#E48CA3",
    edgecolor="#f1eedf",
    width=0.5
)

for bar, (price, count) in zip(
    bars4,
    price_counts.items()
):
    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{count}",
        ha="center",
        fontsize=9,
        color="#343B29"
    )

# медиана

ax4.axhline(
    price_counts.median(),
    color="crimson",
    linestyle="--",
    linewidth=1.5,
    label=f"Медиана: {median_price:.0f}"
)

# аномалия

if len(df_expensive) > 0:
    ax4.annotate(
        f"Аномалия:\n{len(df_expensive)} дорогих товаров",
        xy=(5, max(price_counts.values)),
        xytext=(10, max(price_counts.values) - -0.3),
        arrowprops={
            "arrowstyle": "->",
            "color": "#4B384C"
        },
        fontsize=8,
        color="#4B384C"
    )
stats_text = (
    f"Всего продаж: {len(df_all)}\n"
    f"Среднее: {df_all['price'].mean():.0f}\n"
    f"Медиана: {median_price:.0f}\n"
    f"Мода: {mode_price:.0f}\n"
    f"Ст. откл.: {std_price:.0f}"
)

ax4.text(
    0.97,
    0.95,
    stats_text,
    transform=ax4.transAxes,
    va="top",
    ha="right",
    fontsize=8,
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "lightyellow",
        "edgecolor": "lightgray",
        "alpha": 0.9
    }
)

ax4.set_xlabel("Цена")

ax4.set_ylabel("Количество")

ax4.set_title(
    "Распределение ценочекк",
    fontweight="bold",
    color="#343B29"
)

ax4.legend(fontsize=8)

# аномалия алерт

ax4.text(
    0.5,
    -0.28,
    f"⚠ Аномалия: {len(df_expensive)} товаров "
    f"имеют цену выше третьего квартиля",
    transform=ax4.transAxes,
    fontsize=9,
    color="#FF496C",
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "#FFB3D1",
        "edgecolor": "#BF134F"
    }
)

# сохраняю этот ужас

plt.tight_layout()

OUTPUT_FILE = "sales_charts.png"

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight"
)

print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()

# выводы

print("\n ВЫ(ты)ВОДЫ 🏳️")

top_product = df_products.iloc[0]
worst_product = df_products.iloc[-1]

print(
    f"1. Самая высокая средняя цена у товара "
    f"«{top_product['product']}» "
    f"({top_product['avg_price']})."
)

print(
    f"2. Самая низкая средняя цена у товара "
    f"«{worst_product['product']}» "
    f"({worst_product['avg_price']})."
)

popular_product = df_products.sort_values(
    "total_sales",
    ascending=False
).iloc[0]

print(
    f"3. Самый продаваемый товар — "
    f"«{popular_product['product']}» "
    f"({popular_product['total_sales']} продаж)."
)

print(
    f"4. Средняя цена по всей базе: "
    f"{df_all['price'].mean():.2f}."
)

print(
    f"5. Медианная цена: "
    f"{median_price:.2f}."
)

if len(df_expensive) > 0:
    print(
        f"6. Аномалия!!!: "
        f"{len(df_expensive)} товаров "
        f"имеют слишком высокую цену."
    )
else:
    print("6. Аномалий не найдено.")