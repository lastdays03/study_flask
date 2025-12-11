# Flask 권장 패키지 구조: 기본 vs 마이크로서비스

Flask는 매우 유연한 프레임워크로, 프로젝트의 규모와 목적에 따라 다양한 구조를 취할 수 있습니다. 이 문서는 학습용 또는 소규모 프로젝트를 위한 **기본 패키지 구조**와 대규모 또는 확장성을 고려한 **마이크로서비스(엔터프라이즈) 권장 구조**를 실제 코드 예시와 상세한 주석과 함께 정리합니다.

---

## 1. 기본 패키지 구조 (Basic Package Structure)

단일 파일(`app.py`)에서 시작하여, 템플릿과 정적 파일을 분리하고 코드가 조금 늘어났을 때 권장되는 구조입니다.

### 📂 디렉토리 구조 예시
```
project_root/
├── app.py              # 애플리케이션 진입점 및 실행 파일
├── templates/          # HTML 템플릿 파일 (Jinja2)
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

프로젝트가 커지거나, 여러 개발자가 협업하거나, 기능을 모듈 단위로 분리해야 할 때 사용하는 구조입니다. 핵심은 **애플리케이션 팩토리(Application Factory)** 패턴과 **블루프린트(Blueprint)**의 활용입니다. 이러한 구조는 기능별로 독립성을 높여주어 마이크로서비스 아키텍처로 전환하기에도 유리합니다.

### 📂 디렉토리 구조 상세
```
project_root/
├── .flaskenv               # 환경 변수 (FLASK_APP, FLASK_DEBUG 등 자동 로드)
├── .gitignore              # Git 제외 파일 목록
├── config.py               # [중요] 환경별 설정 (Development, Production, Testing) 분리
├── requirements.txt
├── run.py                  # [중요] 앱 실행 스크립트 (진입점)
├── myapp/                  # 메인 애플리케이션 패키지 (폴더명은 프로젝트명으로 변경 가능)
│   ├── __init__.py         # [중요] Application Factory (create_app) 정의 및 초기화
│   ├── models.py           # 데이터베이스 모델 정의 (SQLAlchemy)
│   ├── templates/          # 전역 공통 템플릿 파일
│   ├── static/             # 전역 공통 정적 파일
│   ├── api/                # [Blueprint] API 관련 기능 모듈
│   │   ├── __init__.py     # Blueprint 객체 생성
│   │   ├── routes.py       # API 엔드포인트 라우팅
│   │   └── schemas.py      # 데이터 검증 및 직렬화 스키마
│   └── auth/               # [Blueprint] 인증 관련 기능 모듈
│       ├── __init__.py
│       ├── routes.py       # 로그인/회원가입 라우팅
│       └── services.py     # 인증 관련 비즈니스 로직
└── tests/                  # 테스트 코드 패키지
    ├── conftest.py         # Pytest 설정 및 공통 Fixture (app, client, db 등)
    ├── test_auth.py
    └── test_api.py
```

### 💻 핵심 파일 작성 예시 및 상세 주석

#### 1) `config.py`: 환경 설정 관리
환경 변수와 설정을 클래스로 관리하여 개발, 테스트, 운영 환경을 명확히 분리합니다.

```python
import os

# 기본 설정 (모든 환경에서 공통)
class Config:
    # 보안 키는 환경 변수에서 가져오되, 없을 경우 개발용 기본값을 사용합니다.
    # 실 서비스에서는 반드시 환경 변수로 설정해야 합니다.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # SQLAlchemy 이벤트 시스템의 불필요한 메모리 사용을 줄이기 위해 끔
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# 개발 환경 설정
class DevelopmentConfig(Config):
    DEBUG = True # 디버거 활성화
    # 개발용 데이터베이스 URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev.db'

# 운영 환경 설정
class ProductionConfig(Config):
    DEBUG = False
    # 운영용 데이터베이스 URI (필수)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# 테스트 환경 설정
class TestingConfig(Config):
    TESTING = True
    # 테스트는 메모리 DB를 사용하여 빠르게 수행하고 격리시킴
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 환경 이름을 키로 하여 설정 클래스를 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig # 기본값
}
```

#### 2) `myapp/__init__.py`: 애플리케이션 팩토리
`create_app` 함수 안에서 앱 인스턴스를 만들고, 확장을 초기화하며, 블루프린트를 등록합니다. 이 패턴을 사용하면 하나의 프로세스에서 여러 설정의 앱을 만들 수 있어 테스트에 유리합니다.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# 1. 확장(Extension)은 전역으로 선언합니다.
# 하지만 아직 앱에 연결되지 않은 상태입니다.
db = SQLAlchemy()

def create_app(config_name='default'):
    """애플리케이션 팩토리 함수"""
    
    # 2. Flask 앱 인스턴스 생성
    app = Flask(__name__)
    
    # 3. 설정 로드: config.py의 딕셔너리에서 환경에 맞는 설정을 가져옴
    app.config.from_object(config[config_name])
    
    # 4. 확장 초기화: 생성된 앱과 확장을 연결합니다(bind).
    db.init_app(app)
    
    # 5. Blueprint 등록
    # 함수 내부에서 import하여 순환 참조(Circular Import) 문제를 방지합니다.
    from myapp.auth import auth_bp
    from myapp.api import api_bp
    
    # url_prefix를 지정하여 하위 경로를 그룹화합니다.
    # 예: auth_bp의 '/login' 라우트는 실제로는 '/auth/login'이 됩니다.
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

#### 3) `run.py`: 실행 엔트리포인트
서버 실행을 담당하는 스크립트입니다. 애플리케이션 팩토리를 호출하여 앱 객체를 생성합니다.

```python
import os
from myapp import create_app

# 환경 변수 FLASK_CONFIG가 없으면 기본값 'default'(=DevelopmentConfig) 사용
config_name = os.getenv('FLASK_CONFIG') or 'default'

# 팩토리 함수를 통해 설정이 적용된 앱 인스턴스 생성
app = create_app(config_name)

if __name__ == '__main__':
    # python run.py 로 직접 실행 시 사용됨
    # 하지만 프로덕션에서는 Gunicorn 등이 app 객체를 import하여 사용함
    app.run()
```

#### 4) Blueprint 정의 (`myapp/auth/__init__.py` 등)
각 기능 모듈을 Blueprint로 만듭니다.

```python
from flask import Blueprint

# Blueprint 객체 생성 ('auth'는 블루프린트의 이름)
auth_bp = Blueprint('auth', __name__)

# 라우트 모듈을 임포트하여 Blueprint와 라우트 함수들을 연결합니다.
# 주의: Blueprint 객체 생성 후에 임포트해야 합니다.
from . import routes
```

### ✅ 마이크로서비스 아키텍처에서의 주요 개념

1.  **모듈화 (Modularity)**: `Blueprint`를 통해 기능(Auth, User, Product 등)을 완전히 분리합니다. 나중에 특정 기능을 별도의 마이크로서비스로 떼어낼 때, 해당 폴더만 분리하면 되므로 리팩토링 비용이 줄어듭니다.
2.  **설정 분리 (Configuration Separation)**: `config.py`를 통해 개발/운영 환경을 코드 수정 없이 환경 변수만으로 전환할 수 있습니다. 이는 Docker와 Kubernetes 환경 배포 시 필수적입니다.
3.  **순환 참조 방지**: 대규모 구조에서는 A가 B를 필요로 하고 B가 A를 필요로 하는 상황이 자주 발생합니다. Application Factory 패턴과 함수 내부 임포트 방식은 이를 효과적으로 해결합니다.

---

## 요약

| 구분 | 기본 구조 | 마이크로서비스/확장 구조 |
| :--- | :--- | :--- |
| **적합한 대상** | 개인 학습, 간단한 토이 프로젝트 | 상용 서비스, 팀 프로젝트, API 서버 |
| **실행 방식** | `app.py` 직접 실행 | `run.py` (Factory 호출) 또는 `flask run` |
| **코드 위치** | 단일 파일 또는 평면적 구조 | 기능별 모듈화 (패키지 + Blueprint) |
| **설정 관리** | 하드코딩 또는 간단한 변수 | 환경 변수 및 `config.py` 클래스 |
