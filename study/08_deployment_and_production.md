# 08. 배포 및 확장 (Deployment & Production)

개발 모드(`flask run --debug`)로 실행하던 애플리케이션을 실제 사용자에게 서비스하기 위해서는 프로덕션 환경에 맞는 배포 설정이 필요합니다.

## 1. WSGI 서버 (Gunicorn)

Flask 내장 서버는 개발용이므로, 보안과 성능을 위해 프로덕션용 WSGI(Web Server Gateway Interface) 서버를 사용해야 합니다. 리눅스/맥 환경에서는 **Gunicorn**이 표준입니다.

**설치**:
```bash
pip install gunicorn
```

**실행**:
```bash
# app.py에 application 객체(또는 app)가 있다고 가정
# -w 4: 워커 프로세스 4개 생성
gunicorn -w 4 app:app
```

## 2. Nginx 설정 (Reverse Proxy)

Gunicorn 앞단에 **Nginx** 웹 서버를 두어 정적 파일 처리, SSL 암호화(HTTPS), 로드 밸런싱 등을 담당하게 합니다.

**구조**:
`Client` -> `Nginx (80/443)` -> `Gunicorn (Unix Socket or 8000)` -> `Flask App`

**Nginx 설정 예시**:
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 3. Docker 컨테이너화

애플리케이션과 실행 환경을 하나로 묶어 어디서든 동일하게 실행되도록 합니다.

**Dockerfile 예시**:
```dockerfile
# 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 실행 명령어 (Gunicorn)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Docker 실행**:
```bash
docker build -t my-flask-app .
docker run -p 5000:5000 my-flask-app
```

## 4. 클라우드 배포 (Cloud Deployment)

### PythonAnywhere
파이썬 전용 호스팅 서비스로, 설정이 매우 간편하여 초보자에게 추천합니다.

### AWS EC2
가상 서버(Ubuntu 등)를 임대하여 직접 Gunicorn, Nginx를 설치하고 설정하는 방식입니다. 완전한 제어가 가능하지만 설정이 복잡합니다.

### AWS Lambda (Serverless) Zappa
서버를 관리하지 않고 코드만 업로드하여 실행하는 서버리스 방식입니다. `Zappa` 라이브러리를 사용하면 Flask 앱을 쉽게 Lambda로 배포할 수 있습니다.
