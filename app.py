from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import random
import math

app = Flask(__name__)
app.secret_key = '1234)'


client = MongoClient(
    'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.5')


db = client['Cube_flask']


users_collection = db['users']
data_collection = db['data']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('input_data'))
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
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password})
            session['username'] = username
            return redirect(url_for('input_data'))
    return render_template('register.html')



@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if 'username' in session:
        if request.method == 'POST':
            n = request.form['n']
            v = request.form['v']
            e = request.form['e']
            session['n'] = n
            session['v'] = v
            session['e'] = e
            return redirect(url_for('generate_r'))
        return render_template('input_form.html')
    return redirect(url_for('index'))


@app.route('/generate_r', methods=['GET', 'POST'])
def generate_r():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        distribution = request.form['distribution']
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])

        if distribution == 'random':
            r = random.random()
        elif distribution == 'gaussian':
            r = abs(np.random.normal())
        elif distribution == 'uniform':
            r = random.uniform(0, 1)

        # Расчет E
        H = 10  # надо будет понять откуда брать h ?
        R = r
        result = H / R if R != 0 else None

        # Расчет объема куба
        volume = x * y * z

        data_collection.insert_one({
            'username': session['username'],
            'distribution': distribution,
            'x': x,
            'y': y,
            'z': z,
            'r': r,
            'result': result,
            'volume': volume
        })

        return render_template('generate_r.html', r=r, result=result, volume=volume)

    return render_template('generate_r.html', r=None, result=None, volume=None)


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if 'username' in session:
        if request.method == 'POST':
            n = request.form['n']
            v = request.form['v']
            e = request.form['e']
            session['n'] = n
            session['v'] = v
            session['e'] = e

            data_collection.insert_one({
                'n' : n,
                'v': v,
                'e': e,
            })
            return redirect(url_for('generate_r'))
        return render_template('input_form.html')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
