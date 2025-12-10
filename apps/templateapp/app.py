from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    current_path = os.getcwd()
    print(current_path)
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
