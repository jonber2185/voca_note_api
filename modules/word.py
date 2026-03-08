import errors.base as _errors
from db import modules as _db_modules


def analyze(set_id: str, words: list) -> list:
    if set_id is None: 
        raise _errors.WordError("set_id is required")
    if words == [] or words is None: 
        raise _errors.WordError("words is required")
    
    return _db_modules.words.analyze(set_id, words)

def getWords(set_id, example = False):
    responses = _db_modules.words.getWords(set_id)
    result = []
    for response in responses:
        meaning = list(map(int, response.get("meaning")))
        wordDetail = _db_modules.words.get_detail(response.get('word_id'))
        definitions = wordDetail.get('definitions', [])

        temp = { 
            "id": wordDetail.get('_id'),
            "word": wordDetail.get("word"),
            "definitions": [{ 
                "ko": definitions[i].get('ko'), 
                "pos": definitions[i].get('pos'),
                "example": definitions[i].get('example', []) if example else None,
            } for i in meaning]
        }
        result.append(temp)
    
    return result

def setWords(set_id, words):
    if words == []: raise _errors.WordError("words is required")
    error_words = []
    for word in words:
        word_id = word.get("word_id")
        meaning = word.get('meaning', [])
        meaning = "".join(map(str, meaning))

        try:
            int(meaning)
            if word_id is None: raise TypeError
            if _db_modules.words.get_detail(word_id) is None: raise TypeError
            if _db_modules.words.getWord(
                set_id=set_id, 
                word_id=word_id
            ) is not None: raise TypeError
        except (TypeError): 
            error_words.append(word)
            continue
        
        _db_modules.words.setWord(
            set_id=set_id,
            word_id=word_id,
            meaning=meaning
        )
    if len(error_words) != 0:
        raise _errors.WordError(
            message="Invalid 'id' or 'meaning' value.",
            payload={ "error_data": error_words }
        )
    
def updateWord(set_id, word):
    if word is None: raise _errors.WordError("word is required")
    word_id = word.get("word_id")
    meaning = word.get('meaning', [])
    meaning = "".join(map(str, meaning))

    try:
        int(meaning)
        if word_id is None: raise TypeError
        if _db_modules.words.get_detail(word_id) is None: raise TypeError
    except TypeError: 
        raise _errors.WordError(message="Invalid 'id' or 'meaning' value.")

    _db_modules.words.updateWord(
        set_id=set_id,
        word_id=word_id,
        meaning=meaning,
    )

from db.modules.words import deleteWord
    