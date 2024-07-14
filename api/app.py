from flask import Flask, render_template
from config import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)


@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/blog')
def blog():  # put application's code here
    return render_template('blog.html')


@app.route('/single_blog')
def single_blog():  # put application's code here
    return render_template('single_blog2.html')


@app.route('/contact')
def contact():  # put application's code here
    return render_template('contact.html')


@app.route('/pdf')
def pdf():  # put application's code here
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
