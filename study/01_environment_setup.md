# 01. 환경 설정 및 시작 (Environment Setup & Basics)

Flask 개발을 시작하기 위한 첫 번째 단계는 개발 환경을 구축하고 기본 애플리케이션을 실행해보는 것입니다.

## 1. Python 가상환경(Virtual Environment) 설정

프로젝트마다 독립적인 패키지 환경을 유지하기 위해 가상환경을 사용합니다.

### Mac/Linux
```bash
# 프로젝트 디렉토리 생성 및 이동
mkdir my_flask_project
cd my_flask_project

# 가상환경 생성 (이름: venv)
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

### Windows
```cmd
:: 프로젝트 디렉토리 생성 및 이동
mkdir my_flask_project
cd my_flask_project

:: 가상환경 생성
python -m venv venv

:: 가상환경 활성화
venv\Scripts\activate
```

가상환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.

## 2. Flask 설치

가상환경이 활성화된 상태에서 `pip`를 사용하여 Flask를 설치합니다.

```bash
pip install Flask
```

설치가 완료되면 버전을 확인해 봅니다.
```bash
flask --version
```

## 3. Hello World 애플리케이션 작성

가장 간단한 Flask 애플리케이션을 만들어 봅니다. 파일명은 보통 `app.py`를 사용합니다.

**파일명: `app.py`**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

- `Flask(__name__)`: 현재 모듈을 기반으로 Flask 앱 인스턴스를 생성합니다.
- `@app.route('/')`: URL 방문 시 어떤 함수를 실행할지 매핑합니다. (여기서는 루트 경로 `/`)
- `app.run(debug=True)`: 개발 서버를 실행합니다. `debug=True`는 코드 변경 시 자동 재시작 및 디버거 기능을 제공합니다.

## 4. 애플리케이션 실행

터미널에서 파이썬 파일을 직접 실행하거나 `flask run` 명령어를 사용할 수 있습니다.

### 방법 1: Python으로 직접 실행
```bash
python app.py
```
`if __name__ == '__main__':` 블록이 실행되어 서버가 켜집니다.

### 방법 2: Flask 명령어로 실행 (권장)
```bash
# 환경 변수 설정 (Mac/Linux)
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run

# 환경 변수 설정 (Windows CMD)
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run
```

브라우저에서 `http://127.0.0.1:5000/`에 접속하여 "Hello, World!"가 보이는지 확인합니다.
