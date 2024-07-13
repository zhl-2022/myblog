from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/myblog-ochre-nu.vercel.app/')
def home():  # put application's code here
    return render_template('index.html')



@app.route('/myblog-ochre-nu.vercel.app/blog')
def blog():  # put application's code here
    return render_template('blog.html')


@app.route('/myblog-ochre-nu.vercel.app/single_blog')
def single_blog():  # put application's code here
    return render_template('single_blog2.html')


@app.route('/myblog-ochre-nu.vercel.app/contact')
def contact():  # put application's code here
    return render_template('contact.html')

@app.route('/myblog-ochre-nu.vercel.app/pdf')
def pdf():  # put application's code here
    return render_template('contact.html')






if __name__ == '__main__':
    app.run(debug=False)
