from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def start():
    context = {
    'title': 'Стартовая страница',
    'content': 'Вы находитесь на главной странице интернет-магазина'
    }
    return render_template(template_name_or_list='index.html', **context)

@app.route('/clothes/')
def clothes():
    context = {
    'title': 'Одежда',
    'content': 'Здесь будет представлен католог с одеждой'
    }
    return render_template(template_name_or_list='clothes.html', **context)

@app.route('/shoes/')
def shoes():
    context = {
    'title': 'Обувь',
    'content': 'Здесь будет представлен католог с обувью'
    }
    return render_template(template_name_or_list='shoes.html', **context)

@app.route('/jacket/')
def jacket():
    context = {
    'title': 'Куртки',
    'content': 'Здесь будет представлен католог с куртками'
    }
    return render_template(template_name_or_list='jacket.html', **context)

if __name__ == "__main__":
    app.run()
