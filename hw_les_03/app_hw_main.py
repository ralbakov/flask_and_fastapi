from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from hw_les_03.models_hw import db, User
from hw_les_03.app_hw_wtforms import RegistrationUser
from werkzeug.security import generate_password_hash #по заданию мы должны сохранить пароль в БД зашифрованным


from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = b'df67be0cc2fe77ba806a33c7f4e469793a456a8a47772bd198cc08bb990ba5f7'
csfr = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def start():
    db.create_all() #для создания базы данных
    print('DataBase create')
    form = RegistrationUser() #get-запрос отрисовывает формы
    if request.method == 'POST' and form.validate(): #post-запрос, получаем данные и загоняем в БД "userdata.db"
        user_name = form.user_name.data
        user_surname = form.user_surname.data
        user_email = form.user_email.data
        user_pass = generate_password_hash(form.user_pass.data)
        user_data = User(user_name=user_name, user_surname=user_surname, user_email=user_email, user_pass=user_pass)
        db.session.add(user_data)
        db.session.commit()
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()