import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


WordRouter = Blueprint('words', __name__)

@WordRouter.route('/analyze', methods=['POST'])
@jwt_required()
def analyzeWords():
    identity = get_jwt_identity()
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    set_id = data.get("set_id")
    modules.set.is_valid_set(set_id, identity)
    responses = modules.word.analyze(set_id, data.get("words", []))
    if responses == []: raise base.WordError("words is empty") 

    result = []
    for response in responses:
        id = response['_id']
        word = response['word']
        definitions_result = []
        definitions = response['definitions']
        for definition in definitions:
            definitions_result.append({ 
                "ko": definition['ko'], 
                "pos": definition["pos"] 
            })
        result.append({
            "id": id,
            "word": word,
            "definitions": definitions_result
        })
    
    return jsonify(result), 200


@WordRouter.route('/<user_id>/<set_id>', methods=['GET'])
@jwt_required(optional=True)
def getWords(user_id, set_id):
    identity = get_jwt_identity()
    user_set = modules.set.get_user_set(set_id, user_id)
    if user_set.get('is_public', 0) == 0 and user_id != identity: 
        raise base.ForbiddenError()
    
    words = modules.word.getWords(set_id)
    
    return jsonify(words), 200
    

@WordRouter.route('/<user_id>/<set_id>/example', methods=['GET'])
@jwt_required(optional=True)
def getWordExamples(user_id, set_id):
    identity = get_jwt_identity()
    user_set = modules.set.get_user_set(set_id, user_id)
    if user_set.get('is_public', 0) == 0 and user_id != identity: 
        raise base.ForbiddenError()
    
    words = modules.word.getWords(set_id, example=True)
    
    return jsonify(words), 200


@WordRouter.route('/<user_id>/<set_id>', methods=['POST'])
@jwt_required()
def addWords(user_id, set_id):
    identity = get_jwt_identity()
    if user_id != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.word.setWords(set_id, data.get("words", []))
    return jsonify({"message": "words updated"}), 200
    

@WordRouter.route('/<user_id>/<set_id>', methods=['PATCH'])
@jwt_required()
def editWords(user_id, set_id):
    identity = get_jwt_identity()
    if user_id != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.word.updateWord(set_id, data.get("word"))
    return jsonify({"message": "words updated"}), 200


@WordRouter.route('/<user_id>/<set_id>/<word_id>', methods=['DELETE'])
@jwt_required()
def deleteWords(user_id, set_id, word_id):
    identity = get_jwt_identity()
    if user_id != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)
    
    modules.word.deleteWord(set_id, word_id)
    return jsonify({"message": "words updated"}), 200
