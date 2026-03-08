from db.mySQL import run_sql


# 아이디 중복 확인
def get_user_id(user_id: str):
    return run_sql(
        "SELECT user_id, username FROM users WHERE user_id = %s",
        (user_id,),
        fetchone=True
    )

def create_user(user_id, username, hashed_password):
    run_sql(
        "INSERT INTO users (user_id, username, pw) VALUES (%s, %s, %s)",
        (user_id, username, hashed_password),
    )

def update_user_password(user_id: str, new_password: str):
    run_sql(
        "UPDATE users SET pw = %s WHERE user_id = %s",
        (new_password, user_id)
    )

def update_username(user_id: str, new_username: str):
    run_sql(
        "UPDATE users SET username = %s WHERE user_id = %s",
        (new_username, user_id)
    )

def delete_user(user_id: str):
    run_sql(
        """
        UPDATE users 
        SET deleted_at = NOW(), 
            user_id = CONCAT(user_id, '_disabled_', UNIX_TIMESTAMP()) 
        WHERE user_id = %s
        """,
        (user_id,)
    )
