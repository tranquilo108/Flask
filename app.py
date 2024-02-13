from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def hello_world():
    return render_template('index.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


@app.route('/jackets/')
def jackets():
    return render_template('jackets.html')


@app.route('/clothes/')
def clothes():
    return render_template('clothes.html')


@app.route('/contact/')
def contact():
    return render_template('contacts.html')


@app.route('/about/')
def about():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run()
