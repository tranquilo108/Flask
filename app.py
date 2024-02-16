import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, make_response

KEY = secrets.token_hex(4)
app = Flask(__name__)
app.secret_key = KEY


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        response = make_response(redirect(url_for('greet')))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)

        return response

    return render_template('index.html')


@app.route('/greet')
def greet():
    user_name = request.cookies.get('user_name')
    user_email = request.cookies.get('user_email')

    return render_template('greet.html', user_name=user_name, user_email=user_email)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')

    return response


if __name__ == '__main__':
    app.run()
