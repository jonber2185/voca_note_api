import re as _re
import errors.base as _errors
from db import modules as _db_modules
from .auth import hash_password as _hash_password


# 조건 정규표현식
allowed_id_pattern = r'^[A-Za-z0-9._-]+$'
allowed_pw_pattern = r'^[A-Za-z0-9!@#$%^&*()\-_+=\[\]{}:;,.?]+$'

# 아이디 조건 확인
def is_valid_user_id(user_id: str):
    if len(user_id) < 4:
        raise _errors.UserValidationError("아이디는 4글자 이상이어야 합니다.")
    if len(user_id) > 30:
        raise _errors.UserValidationError("아이디는 30글자 이하여야 합니다.")
    if ' ' in user_id:
        raise _errors.UserValidationError("공백을 포함할 수 없습니다.")
    if not _re.match(allowed_id_pattern, user_id):
        raise _errors.UserValidationError("아이디는 영문 대소문자, 숫자, 마침표(.), 밑줄(_), 하이픈(-)만 사용할 수 있습니다.")
    
# 아이디 중복 확인
def is_unique_user_id(user_id: str):
    result = _db_modules.users.get_user_id(user_id)
    if result is not None: raise _errors.UserUniqueError()

def is_valid_username(username: str):
    if len(username) > 30:
        raise _errors.UserValidationError("이름은 30글자 이하여야 합니다.")

# pw 조건 확인
def is_valid_password(password: str):
    if len(password) < 8:
        raise _errors.UserValidationError("패스워드는 8글자 이상이어야 합니다.")
    if ' ' in password:
        raise _errors.UserValidationError("패스워드는 공백을 포함할 수 없습니다.")
    if not _re.match(allowed_pw_pattern, password):
        raise _errors.UserValidationError("비밀번호는 영문 대소문자, 숫자, 그리고 특수문자(!@#$%^&*()-_+=[]{}:;,.?)만 사용할 수 있습니다.")


def get_user(user_id):
    userinfo = _db_modules.users.get_user_id(user_id)
    return userinfo

def create_user(user_id, username, password):
    is_valid_user_id(user_id) # id 형식 확인
    is_unique_user_id(user_id) # id 중복 확인
    is_valid_username(username) # username 형식 확인
    is_valid_password(password) # pw 형식 확인

    _db_modules.users.create_user(
        user_id=user_id, 
        username=username,
        hashed_password=_hash_password(password)
    )

def update_user_password(user_id: str, new_password: str):
    is_valid_password(new_password) # pw 형식 확인
    _db_modules.users.update_user_password(
        user_id=user_id,
        new_password=_hash_password(new_password)
    )

def update_username(user_id: str, new_username: str):
    is_valid_username(new_username)
    _db_modules.users.update(
        user_id=user_id,
        new_password=new_username
    )

def delete_user(user_id: str):
    _db_modules.users.delete_user(user_id)