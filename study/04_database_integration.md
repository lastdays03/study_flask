# 04. 데이터베이스 연동 (Database Integration)

Flask는 특정 데이터베이스를 강제하지 않지만, 파이썬 생태계에서 가장 널리 쓰이는 `SQLAlchemy` ORM(Object Relational Helper)을 플라스크에 맞게 래핑한 **Flask-SQLAlchemy**를 주로 사용합니다.

## 1. 설치

```bash
pip install Flask-SQLAlchemy
```

## 2. 설정 및 모델 정의

`app.py` 또는 별도의 파일에서 DB를 설정하고 모델(테이블)을 정의합니다.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# SQLite 데이터베이스 설정 (현재 디렉토리의 site.db 사용)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델 정의 (User 테이블)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

## 3. 데이터베이스 생성

Python 쉘 또는 앱 초기화 시점에 테이블을 생성합니다.
```python
# python shell
from app import app, db
with app.app_context():
    db.create_all() # 모델에 정의된 테이블 생성
```

## 4. CRUD 작업

### Create (생성)
```python
user = User(username='me', email='me@example.com')
db.session.add(user)
db.session.commit()
```

### Read (조회)
```python
all_users = User.query.all()
user = User.query.filter_by(username='me').first()
user_by_id = db.session.get(User, 1) # Flask-SQLAlchemy 3.0+
```

### Update (수정)
```python
user = User.query.first()
user.username = 'new_name'
db.session.commit()
```

### Delete (삭제)
```python
user = User.query.first()
db.session.delete(user)
db.session.commit()
```

## 5. Flask-Migrate (마이그레이션)

데이터베이스 스키마가 변경될 때 테이블을 직접 DROP하고 다시 만드는 대신 마이그레이션 도구를 사용합니다.

**설치**:
```bash
pip install Flask-Migrate
```

**설정**:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

**명령어**:
```bash
flask db init      # 초기 설정 (한 번만 실행)
flask db migrate -m "Initial migration."  # 마이그레이션 스크립트 생성
flask db upgrade   # DB에 적용
```
