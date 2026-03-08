import uuid
import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


SetRouter = Blueprint('set', __name__)

@SetRouter.route('/<username>', methods=['GET'])
@jwt_required(optional=True)
def get_sets(username):
    identity = get_jwt_identity()
    user_sets = modules.set.get_user_sets(username)

    result = []
    if username == identity: result = user_sets
    else: result = [s for s in user_sets if s['is_public'] == 1]
    return jsonify({"sets": result}), 200


@SetRouter.route('/<username>', methods=['POST'])
@jwt_required()
def create_set(username):
    identity = get_jwt_identity()
    if identity != username: raise base.ForbiddenError()

    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")
    
    set_id = uuid.uuid4().hex[:16]
    modules.set.create_set(
        set_id=set_id,
        title=data.get('title', ""),
        description=data.get('description', ""),
        is_public=data.get('is_public', 0),
        owner_id=identity,
    )
    return jsonify({ "message": "set created", "set_id": set_id }), 201


@SetRouter.route('/<username>/<set_id>', methods=['GET'])
@jwt_required(optional=True)
def get_set_detail(username, set_id):
    identity = get_jwt_identity()
    user_set = modules.set.get_user_set(set_id, username)
    if user_set.get('is_public', 0) == 0 and username != identity: 
        raise base.ForbiddenError()
    words = modules.set.getWords(set_id)

    return jsonify({
        "set_info": user_set ,
        "words": words
    }), 200


@SetRouter.route('/<username>/<set_id>', methods=['PATCH'])
@jwt_required()
def update_set_detail(username, set_id):
    identity = get_jwt_identity()
    if identity != username: raise base.ForbiddenError()

    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.set.update_set(
        set_id=set_id,
        owner_id=identity,
        title=data.get('title', ""),
        description=data.get('description', ""),
        is_public=data.get('is_public', 0),
    )

    return jsonify({"message": "set updated successfully"}), 200


@SetRouter.route('/<username>/<set_id>', methods=['DELETE'])
@jwt_required()
def delete_set_detail(username, set_id):
    identity = get_jwt_identity()
    if identity != username: raise base.ForbiddenError()

    modules.set.delete_set(set_id, identity)

    return jsonify({"message": "set deleted successfully"}), 204
