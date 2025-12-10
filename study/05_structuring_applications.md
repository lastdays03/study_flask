# Flask 권장 패키지 구조: 기본 vs 마이크로서비스

Flask는 매우 유연한 프레임워크로, 프로젝트의 규모와 목적에 따라 다양한 구조를 취할 수 있습니다. 이 문서는 학습용 또는 소규모 프로젝트를 위한 **기본 패키지 구조**와 대규모 또는 확장성을 고려한 **마이크로서비스(엔터프라이즈) 권장 구조**를 실제 코드 예시와 함께 정리합니다.

---

## 1. 기본 패키지 구조 (Basic Package Structure)

단일 파일(`app.py`)에서 시작하여, 템플릿과 정적 파일을 분리하고 코드가 조금 늘어났을 때 권장되는 구조입니다.

### 📂 디렉토리 구조 예시
```
project_root/
├── app.py              # 애플리케이션 진입점 및 실행 파일
├── templates/          # HTML 템플릿 파일
│   ├── index.html
│   └── layout.html
├── static/             # 정적 파일 (CSS, JS, Images)
│   ├── style.css
│   └── script.js
├── requirements.txt    # 의존성 패키지 목록
└── .flaskenv           # Flask 환경 변수 설정
```

### 📝 특징
- **단순성**: 모든 로직이 `app.py`에 있거나 최소한으로 분리되어 있어 이해하기 쉽습니다.
- **빠른 프로토타이핑**: 설정이 최소화되어 바로 개발을 시작할 수 있습니다.
- **한계**: 라우트(URL)가 많아지거나 모델이 복잡해지면 `app.py` 파일 하나가 너무 비대해져 유지보수가 어렵습니다.

---

## 2. 마이크로서비스 / 대규모 권장 구조 (Microservice / Scalable Structure)

프로젝트가 커지거나, 여러 개발자가 협업하거나, 기능을 모듈 단위로 분리해야 할 때 사용하는 **애플리케이션 팩토리(Application Factory)** 패턴과 **블루프린트(Blueprint)**를 활용한 구조입니다.

### 📂 디렉토리 구조 상세
```
project_root/
├── .flaskenv               # 환경 변수 (FLASK_APP, FLASK_DEBUG 등)
├── .gitignore
├── config.py               # [중요] 환경별 설정 (Development, Production, Testing)
├── requirements.txt
├── run.py                  # [중요] 앱 실행 스크립트 (entry point)
├── myapp/                  # 애플리케이션 패키지 폴더
│   ├── __init__.py         # [중요] Application Factory (create_app 함수) 정의
│   ├── models.py           # 데이터베이스 모델 (SQLAlchemy 등)
│   ├── templates/          # 공통 템플릿
│   ├── static/             # 공통 정적 파일
│   ├── api/                # [Blueprint] API 관련 기능 모듈
│   │   ├── __init__.py     # Blueprint 생성
│   │   ├── routes.py       # API 라우트 정의
│   │   └── schemas.py      # 데이터 스키마 (Serialization)
│   └── auth/               # [Blueprint] 인증 관련 기능 모듈
│       ├── __init__.py
│       ├── routes.py       # 로그인, 회원가입 라우트
│       └── services.py     # 비즈니스 로직
└── tests/                  # 테스트 코드
    ├── conftest.py         # Pytest 설정 및 Fixtures
    ├── test_auth.py
    └── test_api.py
```

### 💻 핵심 파일 작성 예시

#### 1) `config.py`: 환경 설정 관리
환경 변수와 설정을 클래스로 관리하여 개발, 테스트, 운영 환경을 명확히 분리합니다.

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# config 딕셔너리로 매핑하여 쉽게 선택 가능하게 함
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

#### 2) `myapp/__init__.py`: 애플리케이션 팩토리
`create_app` 함수 안에서 앱 인스턴스를 만들고 설정을 로드하며, 확장(Extension)과 블루프린트를 등록합니다.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# 확장은 전역으로 선언하되, 초기화는 나중에 함
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 설정 로드
    app.config.from_object(config[config_name])
    
    # 확장 초기화
    db.init_app(app)
    
    # Blueprint 등록 (여기서 import 해야 순환 참조 방지)
    from myapp.auth import auth_bp
    from myapp.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

#### 3) `run.py`: 실행 엔트리포인트
실제 서버를 띄울 때 사용하는 파일입니다. `flask run` 명령을 쓸 수도 있지만, 이 파일을 `python run.py`로 직접 실행할 수도 있습니다.

```python
import os
from myapp import create_app

# 환경 변수에서 설정 모드를 가져오거나 기본값 사용
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
```

#### 4) `requirements.txt`: 의존성 파일
프로젝트에 필요한 패키지 목록입니다.

**자동 생성 방법**:
터미널에서 다음 명령어를 실행하면 현재 가상환경에 설치된 모든 패키지 목록을 파일로 저장할 수 있습니다.
```bash
pip freeze > requirements.txt
```

**내용 예시**:
```text
Flask==3.0.0
SQLAlchemy==2.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
```

#### 5) `.flaskenv`: 환경 변수 (python-dotenv가 로드)
```bash
FLASK_APP=run.py
FLASK_DEBUG=1
FLASK_CONFIG=development
```

### 📝 주요 개념 및 특징

- **애플리케이션 팩토리 (Application Factory)**: `create_app()`을 사용하여 앱을 생성하므로 테스트 시 다른 설정(`TestConfig`)으로 여러 개의 앱을 만들 수 있어 테스트가 매우 용이해집니다.
- **블루프린트 (Blueprint)**: 기능 단위(auth, api, main 등)로 코드를 분리하므로 유지보수성이 높아지고, 여러 개발자가 동시에 작업하기 좋습니다.
- **확장성**: 위 구조는 Flask 앱이 커져도 구조가 무너지지 않고, 나중에 `Celery` 비동기 작업이나 `Docker` 컨테이너화 시에도 표준적인 위치(entry point 등)가 명확하여 확장이 쉽습니다.

---

## 요약

| 구분 | 기본 구조 | 마이크로서비스/확장 구조 |
| :--- | :--- | :--- |
| **적합한 대상** | 개인 학습, 간단한 토이 프로젝트 | 상용 서비스, 팀 프로젝트, API 서버 |
| **실행 방식** | `app.py` 직접 실행 | `flask run` 또는 `run.py` (Factory 호출) |
| **코드 위치** | 단일 파일 또는 평면적 구조 | 기능별 모듈화 (패키지 + Blueprint) |
| **설정 관리** | 코드 내 하드코딩 또는 간단한 변수 | `config.py` 클래스 또는 환경 변수 |
