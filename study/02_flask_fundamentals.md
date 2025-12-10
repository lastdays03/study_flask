# 02. Flask 기초 (Flask Fundamentals)

Flask 애플리케이션의 핵심 구성 요소인 URL 라우팅과 템플릿 엔진에 대해 알아봅니다.

## 1. URL 라우팅 (Routing)

`@app.route` 데코레이터를 사용하여 URL과 파이썬 함수를 연결합니다.

### 기본 라우팅
```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello Page'
```

### 동적 URL 파라미터 (Dynamic URL Parameters)
URL의 일부를 변수처럼 사용할 수 있습니다. `<type:variable_name>` 형식을 사용합니다.
- `string` (기본값): 슬래시 없는 텍스트
- `int`: 정수
- `float`: 부동소수점
- `path`: 슬래시를 포함한 문자열

```python
@app.route('/user/<username>')
def show_user_profile(username):
    # username은 문자열로 전달됨
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # post_id는 정수로 전달됨
    return f'Post {post_id}'
```

## 2. 템플릿 엔진 (Templates)

Flask는 Jinja2 템플릿 엔진을 내장하고 있어, HTML 내에 파이썬 로직을 표현할 수 있습니다. 템플릿 파일은 기본적으로 `templates` 폴더에 위치해야 합니다.

### 템플릿 렌더링
`render_template` 함수를 사용합니다.
```python
from flask import Flask, render_template

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

### Jinja2 문법 기초

**변수 출력** (`{{ ... }}`)
```html
<p>Hello, {{ name }}!</p>
```

**제어문** (`{% ... %}`)
```html
{% if name %}
  <h1>Hello, {{ name }}!</h1>
{% else %}
  <h1>Hello, Stranger!</h1>
{% endif %}

<ul>
{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}
</ul>
```

### 템플릿 상속 (Inheritance)
기본 레이아웃(`layout.html`)을 만들고 다른 페이지들이 이를 상속받아 재사용할 수 있습니다.

**layout.html**
```html
<!doctype html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**child.html**
```html
{% extends "layout.html" %}
{% block title %}Index{% endblock %}
{% block content %}
    <h1>This is the index page.</h1>
{% endblock %}
```

## 3. 정적 파일 (Static Files)

CSS, JavaScript, 이미지 등의 파일은 `static` 폴더에 저장합니다. Flask는 `/static` URL로 이 파일들을 제공합니다. URL을 생성할 때는 `url_for` 함수를 사용합니다.

```html
<!-- static/style.css 파일을 링크 -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```
