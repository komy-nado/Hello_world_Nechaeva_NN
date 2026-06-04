from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Главная страница
@app.route("/")
def home():
    return render_template("index.html")


# Среднее
@app.route("/api/value/mean")
def mean():
    value = round(random.uniform(3, 5), 2)

    return jsonify({
        "label": "Средний балл",
        "value": value
    })


# Медиана
@app.route("/api/value/median")
def median():
    value = round(random.uniform(3, 5), 2)

    return jsonify({
        "label": "Медиана",
        "value": value
    })


# Количество
@app.route("/api/value/total")
def total():
    value = random.randint(50, 300)

    return jsonify({
        "label": "Количество студентов",
        "value": value
    })


if __name__ == "__main__":
    app.run(debug=True)