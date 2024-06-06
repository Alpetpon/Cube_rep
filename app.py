from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Подключение к MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.5')
db = client['flask_login_demo']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            return f"Добро пожаловать, {username}!"
        else:
            return "Неправильное имя пользователя или пароль"
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return "Пользователь уже существует"
        else:
            users_collection.insert_one({'username': username, 'password': password})
            return "Пользователь зарегистрирован успешно"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
