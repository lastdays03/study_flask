# flask 패키지에서 Flask 클래스를 가져옵니다.
from flask import Flask, render_template

# Flask 클래스를 인스턴스화하여 app 변수에 할당합니다.
# __name__은 현재 모듈의 이름을 나타내는 내장 변수입니다.
# Flask는 이 이름을 통해 앱의 루트 경로를 파악합니다.
app = Flask(__name__)

# @app.route 데코레이터는 URL과 파이썬 함수를 매핑해줍니다.
# 여기서는 루트 경로('/')로 접속했을 때 index 함수가 호출되도록 설정합니다.
@app.route('/')
def index():
    return 'Hello, World!'

# '/hello' 경로로 접속했을 때 hello 함수가 호출되도록 설정합니다.
# 추가된 라우트 예시입니다.
@app.route('/hello', methods=['GET'], endpoint='hello')
def hello():
    return 'Hello, Flask'

@app.route('/hello', methods=['POST'], endpoint='hello_post')
def hello_post():
    return 'Hello, Flask POST'

@app.route('/hello/<name>', methods=['GET'], endpoint='hello_name')
def hello_name(name):
    return f'Hello, {name}'

@app.route('/hello/<name>', methods=['POST'], endpoint='hello_name_post')
def hello_name_post(name):
    return f'Hello, {name} POST'

@app.route('/name/<name>', methods=['GET'], endpoint='show_name')
def show_name(name):
    return render_template('index.html', name=name)

# 스크립트가 직접 실행될 때만 서버를 실행합니다.
# debug=True 설정은 코드가 변경되면 서버를 자동 재시작하고, 오류 발생 시 디버거를 표시합니다.
if __name__ == '__main__':
    app.run(debug=True)
