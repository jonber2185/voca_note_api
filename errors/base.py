class AppError(Exception):
    def __init__(self, message, status_code, payload: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


### AUTH_ERROR
# 인증 관련 모든 에러
class AuthError(AppError):
    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)

# ID 비번 불일치 에러
class LoginDisagreementError(AuthError):
    def __init__(self):
        super().__init__("아이디 또는 비밀번호가 일치하지 않습니다.")

# 토큰 관련 에러
class SessionTokenError(AuthError):
    def __init__(self, message: str):
        super().__init__(message)

# 로그인 안함 에러
class UnAuthorizedError(AuthError):
    def __init__(self):
        super().__init__("Authentication required.")

# 권한 낮음 에러
class ForbiddenError(AuthError):
    def __init__(self):
        super().__init__("Access denied.", status_code=403)



### USER_ERROR
# user 관련 모든 에러
class UserError(AppError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

# 형식 에러
class UserValidationError(UserError):
    def __init__(self, message: str):
        super().__init__(message)

# ID 중복 에러
class UserUniqueError(UserError):
    def __init__(self):
        super().__init__("중복된 아이디입니다.", status_code=409)


### SET_ERROR
# set 관련 모든 에러
class SetError(AppError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

# 형식 에러
class SetValidationError(SetError):
    def __init__(self, message: str):
        super().__init__(message)



### WORDERROR
# word 관련 모든 에러
class WordError(AppError):
    def __init__(self, message: str, status_code: int = 400, payload: dict | None = None):
        super().__init__(message, status_code, payload)
