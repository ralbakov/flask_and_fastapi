from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    '''
    База данных, содержащая "Имя", "Фамилию", "Email", "Пароль" пользователя
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    user_surname = db.Column(db.String(100), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_pass = db.Column(db.String(100), unique=True, nullable=False)