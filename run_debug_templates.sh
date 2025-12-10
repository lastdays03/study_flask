#!/bin/bash

# 설정: Flask 앱의 경로를 환경 변수로 지정합니다.
export FLASK_APP=apps/templateapp/app.py

# 설정: 디버그 모드를 활성화합니다. (개발 시 유용, 운영 환경에서는 끄는 것이 좋습니다)
# export FLASK_ENV=development # flask 2.0 이전
# 옵션에 따라 디버그 모드 실행 (예: 스크립트 실행 시 `./run_debug_templates.sh --debug`)
if [[ "$1" == "--debug" ]]; then
    export FLASK_DEBUG=1 # Flask 2.0 이후 디버그 모드 활성화
    echo "Flask debug mode enabled."
else
    export FLASK_DEBUG=0 # 기본적으로 디버그 모드 비활성화
    echo "Flask debug mode disabled. Run with '--debug' to enable."
fi

export FLASK_RUN_PORT=8000

# Flask 개발 서버를 실행합니다.
# flask run 명령어를 사용하면 FLASK_APP 환경 변수에 지정된 앱을 실행합니다.
echo "Starting Flask Development Server..."
flask run

# 참고: python apps/minimalapp/app.py 로 직접 실행할 수도 있지만,
# flask run 명령어를 사용하는 것이 Flask 환경 변수 활용 등에 더 표준적인 방법입니다.
