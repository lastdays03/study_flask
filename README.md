# 파이썬 플라스크(Flask) 웹 프로그래밍 학습 로드맵

이 문서는 파이썬의 경량 웹 프레임워크인 Flask를 체계적으로 학습하기 위한 가이드입니다.

## 1단계: 환경 설정 및 시작 (Environment Setup & Basics)
- **목표**: Flask 개발 환경을 구축하고 간단한 웹 애플리케이션을 실행합니다.
- **학습 내용**:
  - Python 가상환경(venv) 설정
  - `pip`를 이용한 Flask 설치
  - "Hello World" 출력하는 최소 애플리케이션 작성 (`app.py`)
  - 개발 서버 실행 및 디버그 모드(`debug=True`) 이해

## 2단계: Flask 기초 (Flask Fundamentals)
- **목표**: URL 라우팅과 템플릿 엔진을 이해합니다.
- **학습 내용**:
  - 라우팅(Routing): `@app.route` 데코레이터, 동적 URL 파라미터 (`<type:variable_name>`)
  - 템플릿 엔진(Jinja2): 변수 출력 `{{ }}`, 제어문 `{% if %}`, `{% for %}`
  - 템플릿 상속(`extends`, `block`)을 통한 레이아웃 재사용
  - 정적 파일(Static Files): CSS, JavaScript, 이미지 파일 관리 (`/static`)

## 3단계: 요청과 응답 처리 (Handling Requests & Responses)
- **목표**: 클라이언트의 데이터를 받고 적절하게 응답하는 방법을 배웁니다.
- **학습 내용**:
  - Request 객체: `request.args` (Query String), `request.form` (Post Data), `request.json`
  - HTTP Methods: GET, POST, PUT, DELETE 메서드 처리
  - Response 객체: `make_response`, 상태 코드 설정, 헤더 조작
  - 리다이렉션(`redirect`)과 에러 처리(`abort`, `errorhandler`)

## 4단계: 데이터베이스 연동 (Database Integration)
- **목표**: 웹 애플리케이션에 데이터를 영구 저장합니다.
- **학습 내용**:
  - SQLite 기초 (파일 기반 DB)
  - **Flask-SQLAlchemy**: ORM(Object Relational Mapping) 설정 및 모델 정의
  - CRUD 작업: 데이터 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)
  - 마이그레이션 관리: **Flask-Migrate** 사용법

## 5단계: 구조적 패턴 (Structuring Applications)
- **목표**: 프로젝트 규모가 커짐에 따라 코드를 체계적으로 관리합니다.
- **학습 내용**:
  - **Blueprint**: 기능별(auth, main, api 등)로 라우트 모듈화
  - **Application Factory Pattern**: `create_app` 함수를 통한 앱 생성
  - 순환 참조(Circular Imports) 방지 및 해결
  - 환경 변수 관리 (`python-dotenv`, config 분리)

## 6단계: 사용자 인증 (User Authentication)
- **목표**: 회원가입, 로그인, 로그아웃 기능을 구현합니다.
- **학습 내용**:
  - 쿠키(Cookie)와 세션(Session)의 차이 및 Flask Session 사용
  - 비밀번호 해싱 (Werkzeug `generate_password_hash`, `check_password_hash`)
  - **Flask-Login**: 사용자 세션 관리, `@login_required` 데코레이터

## 7단계: REST API 개발 (Building REST APIs)
- **목표**: 프론트엔드 프레임워크나 모바일 앱과 통신하는 API 서버를 구축합니다.
- **학습 내용**:
  - RESTful 아키텍처 개념
  - JSON 응답 처리 (`jsonify`)
  - **Flask-RESTX** 또는 **Flask-Smorest** 라이브러리 활용 (선택 사항)
  - API 테스트 (Postman, curl 활용)

## 8단계: 배포 및 확장 (Deployment & Production)
- **목표**: 로컬 개발 환경을 넘어 실제 서버에 애플리케이션을 배포합니다.
- **학습 내용**:
  - WSGI 서버: **Gunicorn**, uWSGI 등을 이용한 배포
  - Reverse Proxy: **Nginx** 설정 및 연동
  - Docker 컨테이너화: `Dockerfile`, `docker-compose.yml` 작성 기초
  - 클라우드 배포 (AWS EC2, PythonAnywhere, Heroku 등) 기초
