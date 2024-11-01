from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# HTML-код формы
form_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Форма заказа</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { width: 90%; max-width: 400px; padding: 20px; border: 1px solid #ccc; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; }
        .form-field { margin-bottom: 15px; }
        .form-field label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-field input, .form-field select, .form-field button { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .form-field button { background-color: #007bff; color: #fff; font-weight: bold; cursor: pointer; border: none; }
        .form-field button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <form action="/submit" method="post">
            <div class="form-field"><label for="firstName">Имя:</label><input type="text" id="firstName" name="first_name" required></div>
            <div class="form-field"><label for="lastName">Фамилия:</label><input type="text" id="lastName" name="last_name" required></div>
            <div class="form-field"><label for="phoneNumber">Номер телефона:</label><input type="tel" id="phoneNumber" name="phone_number" pattern="[0-9]{10}" placeholder="1234567890" required></div>
            <div class="form-field"><label for="comment">Комментарий:</label><input type="text" id="comment" name="comment"></div>
            <div class="form-field"><label for="appointmentDate">Дата и время:</label><input type="datetime-local" id="appointmentDate" name="appointment_date" required></div>
            <div class="form-field"><label for="service">Выберите услугу:</label><select id="service" name="service" required><option value="service1">Услуга 1</option><option value="service2">Услуга 2</option><option value="service3">Услуга 3</option></select></div>
            <div class="form-field"><button type="submit">Сделать заказ</button></div>
        </form>
    </div>
</body>
</html>
'''

# Маршрут для отображения формы
@app.route('/')
def form():
    return render_template_string(form_html)

# Маршрут для обработки отправки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    comment = request.form['comment']
    appointment_date = request.form['appointment_date']
    service = request.form['service']

    # Сохраняем данные в базе данных
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (first_name, last_name, phone_number, comment, appointment_date, service)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, phone_number, comment, appointment_date, service))
    conn.commit()
    conn.close()

    return f"<p>Заказ принят! Спасибо, {first_name}!</p>"

if __name__ == '__main__':
    app.run(debug=True)
