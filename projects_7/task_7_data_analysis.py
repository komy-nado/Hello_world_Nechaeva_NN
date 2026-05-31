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
        password="example",
        database="testdb"
    )

    print("✓ Подключение установлено")

    # SQL1 (балл и количество сдач по курсам)

    df_courses = pd.read_sql("""
        SELECT
            c.course_name AS course,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
            COUNT(e.enrollment_id) AS total_enrollments
        FROM enrollments e
        JOIN courses c
            ON e.course_id = c.course_id
        GROUP BY c.course_name
        ORDER BY avg_grade DESC
    """, connection)

    # SQL2 (в штуках студентов по году поступления)

    df_years = pd.read_sql("""
        SELECT
            enrollment_year AS year,
            COUNT(student_id) AS students
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
    """, connection)

    # SQL3 (все оценки)

    df_all = pd.read_sql("""
        SELECT grade
        FROM enrollments
    """, connection)

    # SQL4 студенты-аномалии

    df_missing = pd.read_sql("""
        SELECT
            s.first_name || ' ' || s.last_name AS student,
            s.enrollment_year
        FROM students s
        LEFT JOIN enrollments e
            ON s.student_id = e.student_id
        WHERE e.enrollment_id IS NULL
        ORDER BY s.enrollment_year, s.last_name
    """, connection)

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто")

# готовлю данные

NAME_MAP = {
    "Основы программирования на Python": "Python",
    "Алгоритмы и структуры данных": "Алгоритмы",
    "Базы данных и SQL": "SQL",
    "Веб-разработка (Frontend)": "Frontend",
    "Администрирование Linux": "Linux",
    "Математический анализ": "Матанализ",
    "Дискретная математика": "Дискр. мат.",
    "Английский язык для IT": "Английский",
}

df_courses["short_name"] = df_courses["course"].map(NAME_MAP)

overall_avg = df_courses["avg_grade"].mean()
median_grade = df_all["grade"].median()
std_grade = df_all["grade"].std()
mode_grade = df_all["grade"].mode()[0]

GRADE_THRESHOLD = 3.8

bar_colors = [
    "#cf580aff" if g < GRADE_THRESHOLD else "#7fdb3dd3"
    for g in df_courses["avg_grade"]
]

pie_labels = [
    f"{row.year} ({row.students} чел.)"
    for _, row in df_years.iterrows()
]

# фигурку рисую.

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("#dfe6d5")
fig.suptitle(
    "Анализ учебной базы данных",
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
# график со средними баллами

bars1 = ax1.barh(
    df_courses["short_name"],
    df_courses["avg_grade"],
    color=bar_colors,
    edgecolor="#f1eedf",
    height=0.6
)

for bar, value in zip(bars1, df_courses["avg_grade"]):
    ax1.text(
        bar.get_width() + 0.03,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}",
        va="center",
        fontsize=9,
        color="#343B29"
    )

ax1.axvline(
    overall_avg,
    color="#642424",
    linestyle="--",
    linewidth=1.5,
    label=f"Среднее по больнице: {overall_avg:.2f}"
)

legend_patches = [
    Patch(facecolor="#7fdb3dd3", label="Норма жизни"),
    Patch(facecolor="#cf580aff", label="Страшная жуткая ужасная болезнь")
]

ax1.legend(handles=legend_patches, fontsize=8)

ax1.set_xlim(1.5, 5.5)
ax1.set_xlabel("Средний балл")
ax1.set_title(
    "Средний балл по курсам",
    fontweight="bold",
    color="#343B29"
)

# график с кол-вом сдач по курсам

bars2 = ax2.bar(
    df_courses["short_name"],
    df_courses["total_enrollments"],
    color="#697e4e",
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

ax2.set_ylim(0, max(df_courses["total_enrollments"]) + 2)

ax2.set_ylabel("Количество сдач")

ax2.set_title(
    "Количество сдач по курсам",
    fontweight="bold",
    color="#343B29"
)

ax2.set_xticks(range(len(df_courses)))

ax2.set_xticklabels(
    df_courses["short_name"],
    rotation=40,
    ha="right",
    fontsize=8
)

# диаграмочка

pie_colors = ["#503d33", "#025e73", "#7f7f48"]

wedges, texts, autotexts = ax3.pie(
    df_years["students"],
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

ax3.legend(
    wedges,
    pie_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.25),
    fontsize=8,
    frameon=False
)

ax3.set_title(
    "Студенты по году поступления",
    fontweight="bold",
    color="#343B29"
)

# график распределения оценочек

grade_counts = df_all["grade"].value_counts().sort_index()

bars4 = ax4.bar(
    grade_counts.index,
    grade_counts.values,
    color="#E48CA3",
    edgecolor="#f1eedf",
    width=0.5
)

for bar, (grade, count) in zip(bars4, grade_counts.items()):
    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.2,
        f"{count} ({count / len(df_all) * 100:.0f}%)",
        ha="center",
        fontsize=9,
        color="#343B29"
    )

# медиана
ax4.axvline(
    median_grade,
    color="crimson",
    linestyle="--",
    linewidth=1.5,
    label=f"Медиана: {median_grade}"
)

# аномалия
if 2 in grade_counts.index:
    ax4.annotate(
        f"Аномалия:\n{grade_counts[2]} оценки «2»",
        xy=(2, grade_counts[2]),
        xytext=(2.4, grade_counts[2] + 4),
        arrowprops={
            "arrowstyle": "->",
            "color": "#ffa000"
        },
        fontsize=8,
        color="#ffa000"
    )

stats_text = (
    f"Всего оценок: {len(df_all)}\n"
    f"Среднее: {df_all['grade'].mean():.2f}\n"
    f"Медиана: {median_grade:.2f}\n"
    f"Мода: {mode_grade}\n"
    f"Ст. откл.: {std_grade:.2f}"
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

ax4.set_xticks([2, 3, 4, 5])
ax4.set_xlabel("Оценка")
ax4.set_ylabel("Количество")

ax4.set_title(
    "Распределение оценочекк",
    fontweight="bold",
    color="#343B29"
)

ax4.legend(fontsize=8)

# аномалия алерт
fig.text(
    0.5,
    -0.03,
    f"⚠ Аномалия: {len(df_missing)} студентов "
    f"не имеют записей в таблице enrollments",
    ha="center",
    fontsize=9,
    color="#C21E56",
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "#cddab2",
        "edgecolor": "#e48b61ff"
    }
)

# сохраняю этот ужас
plt.tight_layout()

OUTPUT_FILE = "student_charts.png"

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight"
)

print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()

# выводы

print("\n ВЫ(ты)ВОДЫ 🏳️")

top_course = df_courses.iloc[0]
worst_course = df_courses.iloc[-1]

print(
    f"1. Лучший средний балл у курса "
    f"«{top_course['course']}» "
    f"({top_course['avg_grade']})."
)

print(
    f"2. Самый низкий средний балл у курса "
    f"«{worst_course['course']}» "
    f"({worst_course['avg_grade']})."
)

popular_course = df_courses.sort_values(
    "total_enrollments",
    ascending=False
).iloc[0]

print(
    f"3. Самый популярный курс — "
    f"«{popular_course['course']}» "
    f"({popular_course['total_enrollments']} сдач)."
)

print(
    f"4. Средняя оценка по всей базе: "
    f"{df_all['grade'].mean():.2f}."
)

print(
    f"5. Медианная оценка: "
    f"{median_grade:.2f}."
)

if len(df_missing) > 0:
    print(
        f"6. Аномалия!!!: "
        f"{len(df_missing)} лоботрясов "
        f"не имеют оценок."
    )
else:
    print("6. Лоботрясов не найдено.")