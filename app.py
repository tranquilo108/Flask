import hashlib
import secrets

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegistrationForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
@app.route('/index/')
def index():
    return render_template('base.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form)
    print(app.config['SECRET_KEY'])

    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        password = hashlib.md5(password.encode()).hexdigest()
        user = User.query.filter_by(email=email).first()

        if user:
            form.email.data = 'Такая почта уже зарегистрирована'
            return render_template('register.html', form=form)

        else:
            user = User(firstname=firstname, lastname=lastname, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return 'Регистрация прошла успешно!'

    return render_template('register.html', form=form)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


if __name__ == '__main__':
    app.run()
