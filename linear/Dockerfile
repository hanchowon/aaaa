# 파이썬 3.11 경량화 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 전체 복사
COPY . .

# Cloud Run 기본 포트 설정
ENV PORT=8080

# Gunicorn WSGI 서버 실행 (프로덕션 환경 대응)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
