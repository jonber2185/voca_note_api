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
    
    # 1. DB에서 기존 단어들을 한꺼번에 조회 ($in 연산자 사용)
    existing_docs = list(_word_list.find({"word": {"$in": words}}))
    existing_map = {doc['word']: doc for doc in existing_docs}
    
    gemini_words = []
    for word in words:
        if word in existing_map:
            data = existing_map[word]
            # getWord 로직 유지 (캐시나 특정 세션 확인용인 것으로 보임)
            response = getWord(set_id=set_id, word_id=data['_id'])
            if response is None: 
                result.append(data)
        else:
            gemini_words.append(word)

    # 2. 새로운 단어가 있을 때만 AI 분석 실행
    if gemini_words:
        word_chunks = [gemini_words[i:i + _chunk_len] for i in range(0, len(gemini_words), _chunk_len)]
        futures = [_word_executor.submit(_get_gemini_response, word_chunk) for word_chunk in word_chunks]
        
        new_items_to_db = []
        for future in futures:
            try:
                # 여기서 AI 응답 대기 (Timeout 주의)
                future_result = future.result(timeout=60) 
                if not future_result: continue
                
                for item in future_result:
                    item['_id'] = _uuid.uuid4().hex[:16]
                    new_items_to_db.append(item)
                    result.append(item)
            except Exception as e:
                print(f"AI 분석 중 오류 발생: {e}")

        # 3. DB 삽입 최적화
        if new_items_to_db:
            try:
                _word_list.insert_many(new_items_to_db, ordered=False)
            except _BulkWriteError:
                # 중복된 ID 등이 있을 경우 예외 처리 (필요시)
                pass

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
    