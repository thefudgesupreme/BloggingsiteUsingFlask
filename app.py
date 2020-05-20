from flask import Flask, render_template,url_for

app = Flask(__name__)

posts = [
    {
        'author': "Vipul",
        'title': "About author",
        'date': "April 10, 2020"
    },
    {
        'author': "Vipul",
        'title': "First Post",
        'date': "April 12, 2020"
    }
]


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('home.html', title="  Home", posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


if __name__=='__main__':
    app.run(debug=True)
