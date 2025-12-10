from flask import Flask, render_template, url_for
import os

app = Flask(__name__)
current_path = os.getcwd()
print('current_path: ', current_path)

@app.route('/', methods=['GET'], endpoint='index')
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'], endpoint='about')
def about():
    context = {
        'name': 'Flask',
        'version': '2.0.1',
        'users': ['user1', 'user2', 'user3']
    }
    return render_template('about.html', **context)

@app.route('/user/<username>', methods=['GET'], endpoint='user')
def user(username):
    return render_template('user.html', username=username)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('about', ccc=123))
    print(url_for('user', username='Flask', abc=123))