import uuid as _uuid
from db.mySQL import run_sql as _run_sql
from db.mongo import db_connection as _db_connection
from modules.gemini import get_gemini_response as _get_gemini_response
from pymongo.errors import BulkWriteError as _BulkWriteError
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor


_word_list = _db_connection()
_word_executor = _ThreadPoolExecutor(max_workers=4)
_chunk_len = 10

def analyze(set_id: str, words: list) -> list:
    result = []
    gemini_words = []
    for word in words:
        data = _word_list.find_one({"word": word})
        if data is not None:
            response = getWord(set_id=set_id, word_id=data['_id'])
            if response is None: result.append(data)
        else: gemini_words.append(word)

    if gemini_words is not None:
        word_chunks = [gemini_words[i:i + _chunk_len] for i in range(0, len(gemini_words), _chunk_len)]
        futures = [_word_executor.submit(_get_gemini_response, word_chunk) for word_chunk in word_chunks]
        
        # future ended
        for future in futures:
            future_result = future.result()
            if future_result is None or future_result == []: continue
            for item in future_result:
                item['_id'] = _uuid.uuid4().hex[:16]
            result.extend(future_result)

            # insert db
            try:
                _word_list.insert_many(future_result, ordered=False)
            except _BulkWriteError as bwe:
                write_errors = bwe.details.get('writeErrors', [])
                for error in write_errors:
                    failed_index = error['index']
                    failed_item = future_result[failed_index]
                    failed_item['_id'] = _uuid.uuid4().hex[:16]
                    _word_list.insert_one(failed_item)

    return result

def get_detail(word_id):
    data = _word_list.find_one({"_id": word_id})
    return data

def getWord(set_id, word_id) -> dict:
    result = _run_sql(
        "SELECT word_id, meaning FROM words WHERE set_id = %s AND word_id = %s",
        (set_id, word_id),
        fetchone=True
    )
    return result

def getWords(set_id) -> list:
    results = _run_sql(
        "SELECT word_id, meaning FROM words WHERE set_id = %s",
        (set_id,),
    )
    return results

def setWord(set_id, word_id, meaning):
    _run_sql(
        "INSERT INTO words (set_id, word_id, meaning) VALUES (%s, %s, %s)",
        (set_id, word_id, meaning)
    )

def updateWord(set_id, word_id, meaning):
    _run_sql(
        "UPDATE words SET meaning = %s WHERE set_id = %s AND word_id = %s",
        (meaning, set_id, word_id)
    )

def deleteWord(set_id, word_id):
    _run_sql(
        "DELETE FROM words WHERE set_id = %s AND word_id = %s", 
        (set_id, word_id)
    )
    