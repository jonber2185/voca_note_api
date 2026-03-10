import bcrypt as _bcrypt
import errors.base as _errors
from hashlib import sha256 as _sha256
from db import modules as _db_modules
from flask_jwt_extended import (
    create_access_token as _create_access_token, 
    create_refresh_token as _create_refresh_token
)


### login

def hash_password(password: str) -> str:
    salt = _bcrypt.gensalt()
    hashed = _bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') # DB에 저장할 문자열

def login(input_id: str, input_password: str):
    # 타입 확인
    from . import user as _user
    _user.is_valid_user_id(input_id) # id 형식 확인
    _user.is_valid_password(input_password) # pw 형식 확인

    # 실제 pw 가져오기
    user_info = _db_modules.auth.get_password_by_input_id(input_id)
    if user_info is None or user_info.get("deleted_at") is not None: 
        raise _errors.LoginDisagreementError()
    user_password = user_info.get("pw")

    # pw 확인
    isCorrect = _bcrypt.checkpw(
        password=input_password.encode('utf-8'), 
        hashed_password=user_password.encode('utf-8')
    )
    if not isCorrect: raise _errors.LoginDisagreementError()


### tokens

def login_tokens(identity: str, device_id: str) -> list:
    if device_id is None:
        raise _errors.SessionTokenError("device_id is empty")
    if len(device_id) > 20:
        raise _errors.SessionTokenError("device_id must be 20 or less")
        
    # token 발급
    access_token = _create_access_token(identity=identity)
    refresh_token = _create_refresh_token(identity=identity)
    new_hashed_refresh_token = _sha256(refresh_token.encode()).hexdigest()  

    # db에 새로운 refresh_token 저장
    _db_modules.auth.set_new_refresh_token(
        user_id=identity, 
        device_id=device_id,
        token=new_hashed_refresh_token
    )

    #token 반환
    return [access_token, refresh_token]

def update_tokens(input_refresh_token: str, identity: str, device_id: str) -> list:
    # refresh_token 유효 검증
    if not input_refresh_token:
        raise _errors.SessionTokenError("refresh token is required")
    if device_id == "":
        raise _errors.SessionTokenError("device_id is empty")

    hashed_refresh_token = _sha256(input_refresh_token.encode()).hexdigest()    
    stored_refresh_token = _db_modules.auth.get_token_by_user_id(identity, device_id)

    if stored_refresh_token != hashed_refresh_token:
        raise _errors.SessionTokenError("Invalid refresh token")

    # token 발급
    access_token = _create_access_token(identity=identity)
    refresh_token = _create_refresh_token(identity=identity)
    new_hashed_refresh_token = _sha256(refresh_token.encode()).hexdigest()  

    # db에 새로운 refresh_token 저장
    _db_modules.auth.set_new_refresh_token(
        user_id=identity, 
        device_id=device_id,
        token=new_hashed_refresh_token
    )

    # refresh_token 반환
    return [access_token, refresh_token]

from db.modules.auth import delete_refresh_token as delete_tokens