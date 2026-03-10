import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

UserRouter = Blueprint('user', __name__)


@UserRouter.route('/me', methods=['GET'])
@jwt_required()
def webRefresh():
    identity = get_jwt_identity()

    return jsonify({
        "user_id": identity,
    }), 200

@UserRouter.route('/create', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if data is None: raise base.UserValidationError("data empty.")

    user_id = data.get('user_id')
    password = data.get('password')
    if not all([user_id, password]):
        raise base.UserValidationError("Invalid format.")

    modules.user.create_user(
        user_id=user_id,
        password=password
    )
    return jsonify({"message": "user created"}), 201


@UserRouter.route('/update_password',methods=['POST'])
@jwt_required()
def update_user_password():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True)
    if data is None: raise base.UserValidationError("empty data.")
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not all([current_password, new_password]):
        raise base.UserValidationError("Missing required argument.")
    
    modules.auth.login(input_id=user_id, input_password=current_password)
    modules.user.update_user_password(
        user_id=user_id,
        new_password=new_password
    )
    return jsonify({ "message": "Profile updated successfully." }), 201


@UserRouter.route('/delete',methods=['POST'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True)
    if data is None: raise base.UserValidationError("empty data.")
    input_password = data.get('password')

    if not input_password:
        raise base.UserValidationError("password is required")
    
    modules.auth.login(input_id=user_id, input_password=input_password)
    
    modules.auth.delete_tokens(user_id)
    modules.user.delete_user(user_id)
    return jsonify({ "message": "Profile deleted." }), 203