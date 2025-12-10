# 06. 사용자 인증 (User Authentication)

대부분의 웹 애플리케이션은 회원가입, 로그인, 로그아웃과 같은 사용자 인증 기능을 필요로 합니다. Flask에서는 `Session`을 기본 제공하며, **Flask-Login** 확장을 통해 더 편리하게 인증 시스템을 구축할 수 있습니다.

## 1. 쿠키(Cookie)와 세션(Session)

### 쿠키 (Cookie)
클라이언트(브라우저)에 저장되는 키-값 쌍의 작은 데이터입니다.
```python
from flask import make_response

@app.route('/set_cookie')
def set_cookie():
    resp = make_response('Cookie set')
    resp.set_cookie('username', 'the_user')
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return username
```

### 세션 (Session)
서버에 저장되는(또는 암호화되어 쿠키에 저장되는) 사용자 별 데이터입니다. Flask의 기본 세션은 **클라이언트 사이드 세션**으로, 데이터가 서명된 쿠키(Signed Cookie)에 저장됩니다. 따라서 `SECRET_KEY` 설정이 필수입니다.

```python
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'super-secret-key' # 필수 설정

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None) # 세션 제거
    return redirect(url_for('index'))
```

## 2. 비밀번호 해싱 (Password Hashing)

비밀번호는 절대 평문으로 저장해서는 안 됩니다. `Werkzeug`의 보안 유틸리티를 사용합니다.

```python
from werkzeug.security import generate_password_hash, check_password_hash

# 회원가입 시: 비밀번호 해시 생성
password = "my_password"
pw_hash = generate_password_hash(password)
# pw_hash 예시: 'pbkdf2:sha256:260000$...' (DB에 저장)

# 로그인 시: 비밀번호 검증
is_correct = check_password_hash(pw_hash, "my_password") # True
is_wrong = check_password_hash(pw_hash, "wrong_password") # False
```

## 3. Flask-Login 확장

사용자 세션 관리(로그인 상태 유지, `@login_required` 등)를 쉽게 해주는 확장입니다.

**설치**:
```bash
pip install Flask-Login
```

**설정 및 사용**:
1. **User 클래스**: `UserMixin` 상속
2. **LoginManager**: 앱에 등록 및 `user_loader` 콜백 함수 정의
3. **로그인/로그아웃**: `login_user()`, `logout_user()` 함수 사용

```python
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # 로그인 페이지의 뷰 함수 이름

class User(UserMixin):
    # 실제로는 DB 모델이어야 함
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # DB에서 user_id로 사용자 조회 후 User 객체 반환
    return User(user_id) 

@app.route('/login', methods=['POST'])
def login():
    # ... 사용자 검증 로직 ...
    user = User(user_id)
    login_user(user) # 로그인 처리
    return redirect(url_for('index'))

@app.route('/protected')
@login_required # 로그인한 사용자만 접근 가능
def protected():
    return f'Logged in as: {current_user.id}'

@app.route('/logout')
@login_required
def logout():
    logout_user() # 로그아웃
    return 'Logged out'
```
