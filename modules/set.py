import errors.base as _errors
from pymysql.err import IntegrityError as _IntegrityError
from db import modules as _db_modules


def is_valid_set(set_id, identity):
    response = get_user_set(set_id, identity)
    if response == {}: raise _errors.SetValidationError("set doesn't exist")


def create_set(set_id, title, description, owner_id, is_public):
    if title == "":
        raise _errors.SetValidationError("title is required")
    if len(title) > 100:
        raise _errors.SetValidationError("title must be 100 characters or less.")
    if len(description) > 250:
        raise _errors.SetValidationError("description must be 250 characters or less.")
    if is_public != 0 and is_public != 1:
        raise _errors.SetValidationError("is_public must be 0 or 1.")

    try:
        _db_modules.sets.create_set(
            set_id=set_id,
            title=title,
            description=description,
            is_public=is_public,
            owner_id=owner_id,
        )
    except _IntegrityError as e:
        if e.args[0] == 1062:
            raise _errors.SetError("set already exist.") 
        raise e
    
def update_set(set_id, owner_id, title=None, description=None, is_public=None):
    if title is not None and len(title) > 100:
        raise _errors.SetValidationError("title must be 100 characters or less.")
    if description is not None and len(description) > 250:
        raise _errors.SetValidationError("description must be 250 characters or less.")
    if is_public is not None and is_public != 0 and is_public != 1:
        raise _errors.SetValidationError("is_public must be 0 or 1.")

    _db_modules.sets.update_set(
        set_id=set_id,
        owner_id=owner_id,
        title=title,
        description=description,
        is_public=is_public,
    )


from db.modules.sets import (search_set, get_user_set, get_user_sets, delete_set)


def getWords(set_id):
    responses = _db_modules.words.getWords(set_id)
    result = []
    for response in responses:
        meaning = list(map(int, response.get("meaning")))
        wordDetail = _db_modules.words.get_detail(response.get('word_id'))
        definitions = wordDetail.get('definitions', [])

        temp = { 
            "id": wordDetail.get('_id'),
            "word": wordDetail.get("word"),
            "meaning": meaning,
            "ko": [definition.get('ko') for definition in definitions]
        }
        result.append(temp)
    
    return result