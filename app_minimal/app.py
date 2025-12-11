import os
import logging
from flask import Flask, render_template, url_for, request, redirect, flash, make_response, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError

# --- Flask 애플리케이션 초기화 ---
app = Flask(__name__)

# --- 환경 설정 (Configuration) ---
# 보안 키 설정 (세션 및 플래시 메시지 사용에 필수)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# 디버그 툴바 설정: 리다이렉트 인터셉트 끄기 (페이지 이동 시 중간 멈춤 방지)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# 이메일 전송 설정 (환경 변수에서 로드)
app.config['MAIL_SERVER'] = os.environ.get('SMTP_SERVER')
app.config['MAIL_PORT'] = os.environ.get('SMTP_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('SMTP_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('SMTP_DEFAULT_SENDER')

# --- 확장(Extensions) 초기화 ---
# Flask-DebugToolbar: 디버깅 도구 모음
toolbar = DebugToolbarExtension(app)

# Flask-Mail: 이메일 발송 기능
mail = Mail(app)

# --- 유틸리티: 현재 실행 경로 확인 ---
# 디버깅 용도로 현재 작업 디렉토리를 출력
# current_path = os.getcwd()
# print('current_path: ', current_path)

# --- 라우트 정의 (Routes) ---

@app.route('/', methods=['GET'], endpoint='index')
def index():
    cookie_username = request.cookies.get('username')
    session_username = session.get('username')
    print(cookie_username)
    print(session_username)
    """메인 페이지 렌더링"""
    return render_template('index.html')

@app.route('/about', methods=['GET'], endpoint='about')
def about():
    """소개 페이지: 템플릿에 데이터(Context) 전달 예시"""
    context = {
        'name': 'Flask',
        'version': '2.0.1',
        'users': ['user1', 'user2', 'user3']
    }
    # **context를 사용하여 딕셔너리를 키워드 인자로 풀어서 전달
    return render_template('about/about.html', **context)

@app.route('/user/<username>', methods=['GET'], endpoint='user')
def user(username):
    """동적 URL 파라미터 처리 예시 (사용자 프로필)"""
    return render_template('user/user.html', username=username)

@app.route('/cookie/set', methods=['GET'], endpoint='set_cookie_session')
def set_cookie_session():
    """쿠키와 세션을 설정하는 라우트"""
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', 'test_cookie_user', max_age=3600)
    session['username'] = 'test_session_user'
    flash('쿠키와 세션이 설정되었습니다.')
    return response

@app.route('/cookie/delete', methods=['GET'], endpoint='delete_cookie_session')
def delete_cookie_session():
    """쿠키와 세션을 삭제하는 라우트"""
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    session.pop('username', None)
    flash('쿠키와 세션이 삭제되었습니다.')
    return response

@app.route('/contact', methods=['GET'], endpoint='contact')
def contact():
    """문의 페이지 렌더링 및 로깅 테스트"""
    # 다양한 로그 레벨 테스트
    app.logger.debug('Debug log test')
    app.logger.info('Info log test')
    app.logger.warning('Warning log test')
    app.logger.error('Error log test')
    app.logger.critical('Critical log test')
    
    return render_template('contact/contact.html')

@app.route('/contact/complete', methods=['GET', 'POST'], endpoint='contact_complete')
def contact_complete():
    """문의 제출 처리 및 완료 페이지"""
    
    if request.method == 'POST':
        # 1. 폼 데이터 수신
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # 2. 유효성 검사 (Validation)
        errors = {}
        try:
            # 이메일 형식 검증 (email-validator 패키지 사용)
            v = validate_email(email)
            email = v["email"] # 정규화된 이메일 주소 사용
        except EmailNotValidError as e:
            errors['email'] = str(e)
            app.logger.error(f'Email validation error: {str(e)}')

        # 에러 발생 시 처리
        if errors:
            flash('이메일 형식이 올바르지 않습니다.')
            # 입력값을 유지하려면 폼 데이터를 다시 템플릿으로 전달할 수 있음 (여기선 생략)
            return render_template('contact/contact.html')

        # 3. 이메일 발송 (비동기 처리는 Celery 등을 사용해야 함)
        send_contact_email(name, email, subject, message)
        
        # 4. 성공 메시지 및 리다이렉트
        flash('문의가 성공적으로 접수되었습니다.')
        app.logger.info(f'Contact form submitted by: {email}')
        
        # PRG (Post-Redirect-Get) 패턴: 새로고침 시 중복 제출 방지
        return redirect(url_for('contact_complete'))
        
    # GET 요청 시 완료 페이지 렌더링
    return render_template('contact/contact_complete.html')

def send_contact_email(name, email, subject, message):
    """이메일 발송 헬퍼 함수"""
    msg = Message(subject, sender=email, recipients=[email])
    msg.html = render_template('contact/contract_mail.html', 
                             name=name, 
                             email=email, 
                             subject=subject,
                             message=message)
    mail.send(msg)

# --- 애플리케이션 실행 ---
if __name__ == '__main__':
    # debug=True: 코드 수정 시 자동 재시작 및 디버거 활성화
    app.run(debug=True, port=8000)

# --- 테스트 컨텍스트 예시 (주석 처리됨) ---
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('user', username='Flask'))