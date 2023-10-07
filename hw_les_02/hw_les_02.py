'''
Задание
Создать страницу, на которой будет форма для ввода имени и электронной почты, 
при отправке которой будет создан cookie-файл с данными пользователя, 
а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», 
при нажатии на которую будет удалён cookie-файл с данными пользователя и 
произведено перенаправление на страницу ввода имени и электронной почты.
'''

from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.secret_key = b'df67be0cc2fe77ba806a33c7f4e469793a456a8a47772bd198cc08bb990ba5f7'

@app.route('/', methods=['GET', 'POST'])
def start():
    context = {
    'title': 'Start page',
    'content': 'Стартовая страница'
    }
    response = make_response(render_template('index.html', **context))
    response.delete_cookie('user')
    response.delete_cookie('email')
    return response

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        user = request.form.get('user')
        email = request.form.get('email')
        context = {
        'title': 'Welcome page',
        'user': user,
        'email': email
        }
        response = make_response(render_template('welcome.html', **context))
        response.set_cookie('user', context['user'])
        response.set_cookie('email', context['email'])
    return response

if __name__ == "__main__":
    app.run(debug=True)