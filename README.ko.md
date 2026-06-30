# VocaNote API

[English](README.md)

단어 학습 노트 서비스인 **[VocaNote](https://github.com/jonber2185/VocaNote-web)** 의 백엔드 API 서버입니다. 사용자는 단어 세트를 만들고, 단어를 추가/관리하며, Gemini를 이용한 AI 단어 분석(뜻/예문)을 받고, 공개된 세트를 검색할 수 있습니다.

## 기술 스택

| 개요 | 기술 |
|---|---|
| Flask | 웹 프레임워크 |
| Flask-JWT-Extended | HttpOnly 쿠키 기반 인증 (Access/Refresh 토큰) |
| MySQL (PyMySQL) | 관계형 데이터 (사용자, 세트, 세션) |
| MongoDB (PyMongo) | 단어 데이터 |
| Google Gemini (`google-genai`) | 단어/뜻 분석 |
| Gunicorn | 프로덕션 WSGI 서버 |

## API 개요

| 경로 | 설명 |
|---|---|
| `POST /auth/login` | 로그인, JWT 쿠키 발급 |
| `POST /auth/refresh` | 액세스 토큰 갱신 |
| `POST /auth/logout` | 로그아웃, 쿠키 삭제 |
| `GET /user/me` | 현재 사용자 정보 조회 |
| `POST /user/create` | 회원가입 |
| `POST /user/update_password` | 비밀번호 변경 |
| `POST /user/delete` | 회원 탈퇴 |
| `GET/POST /set/<user_id>` | 단어 세트 목록 조회 / 생성 |
| `GET/PATCH/DELETE /set/<user_id>/<set_id>` | 세트 조회 / 수정 / 삭제 |
| `POST /words/analyze` | 단어 목록 AI 분석 |
| `GET/POST/PATCH /words/<user_id>/<set_id>` | 세트 내 단어 조회 / 추가 / 수정 |
| `GET /words/<user_id>/<set_id>/example` | 예문 조회 |
| `DELETE /words/<user_id>/<set_id>/<word_id>` | 단어 삭제 |
| `GET /search?q=` | 사용자/세트 검색 |

## 설치 및 실행

### 요구 사항

- Python 3.10+
- MySQL 데이터베이스
- MongoDB 데이터베이스
- Google Gemini API 키

### 설치

```bash
pip install -r requirements.txt
```

### 환경 변수

프로젝트 루트에 `.env` 파일을 생성하세요.

```env
FRONT_URL=http://localhost:3000
JWT_SECRET_KEY=your-secret-key

MySQL_HOST=localhost
MySQL_USER=your-mysql-user
MySQL_PASSWORD=your-mysql-password
MySQL_NAME=your-database-name
MySQL_PORT=3306

Mongo_ID=your-mongo-username
Mongo_PASSWORD=your-mongo-password

GEMINI_API_KEY=your-gemini-api-key
```

### 실행

```bash
# 개발 환경
python app.py

# 프로덕션 환경
gunicorn app:app
```

## 인증 방식

JWT Access/Refresh 토큰을 `HttpOnly`, `Secure`, `SameSite=None` 속성의 쿠키에 저장하는 방식으로, 프론트엔드와 도메인이 다른 크로스 오리진 환경에 적합합니다.
