import errors.base as base
import modules
from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    set_access_cookies, 
    set_refresh_cookies, 
    unset_jwt_cookies,
)


AuthRouter = Blueprint('auth', __name__)

@AuthRouter.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None: raise base.AuthError("empty data.")

    # id, pw 가져오기
    input_id = data.get('user_id')
    input_password = data.get('password')
    device_id = data.get('device_id')
    if not all([input_id, input_password]):
        raise base.AuthError("ID or password cannot be empty.")

    # 로그인 시도. 실패 시 raise
    modules.auth.login(input_id=input_id, input_password=input_password)

    # 토큰 발급
    [access_token, refresh_token] = modules.auth.login_tokens(input_id, device_id)

    # token return
    response_data = jsonify({
        "user_id": input_id,
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    response = make_response(response_data, 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@AuthRouter.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def webRefresh():
    identity = get_jwt_identity()
    data = request.get_json(silent=True)
    if data is None: raise base.AuthError("empty data.")
    input_refresh_token = request.cookies.get("refresh_token")

    if not input_refresh_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            input_refresh_token = auth_header.split(" ")[1]

    # token 발급
    [new_access_token, new_refresh_token] = modules.auth.update_tokens(
        input_refresh_token=input_refresh_token,
        device_id=data.get('device_id', ""),
        identity=identity,
    )

    if request.cookies.get("refresh_token"):
        response_data = jsonify({"message": "Successfully refreshed."})
        response = make_response(response_data, 200)
        set_access_cookies(response, new_access_token)
        set_refresh_cookies(response, new_refresh_token)
        return response

    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }), 200


@AuthRouter.route('/logout', methods=['POST'])
def logout():
    identity = get_jwt_identity()

    if identity:
        data = request.get_json(silent=True) or {}
        device_id = data.get('device_id', "")
        if device_id:
            modules.auth.delete_tokens(user_id=identity, device_id=device_id)

    response = jsonify({
        "message": "Successfully logged out."
    })
    
    unset_jwt_cookies(response)

    return response, 200
