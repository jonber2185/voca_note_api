import modules
from flask import Blueprint, request, jsonify


SearchRouter = Blueprint('search', __name__)


@SearchRouter.route('/', methods=['GET'])
def getWords():
    query = request.args.get('q')

    user_response = modules.set.get_user_sets(user_id=query)
    set_responses = modules.set.search_set(title=query)

    result = {
        'user': user_response,
        'sets': []
    }
    
    for set_response in set_responses:
        if set_response.get('is_public', 0) == 1:
            result['sets'].append(set_response)

    return jsonify(result), 200
    
