from db.mySQL import run_sql


### password

def get_password_by_input_id(input_id: str) -> dict:
    result = run_sql(
        "SELECT pw, deleted_at FROM users WHERE user_id = %s",
        (input_id,),
        fetchone=True
    )
    return result

### token

def get_token_by_user_id(user_id: str, device_id: str) -> str:
    result = run_sql(
        "SELECT refresh_token FROM refresh_tokens WHERE user_id = %s AND device_id = %s",
        (user_id, device_id),
        fetchone=True
    )
    if result is None: return ""
    return result.get('refresh_token', "")

def set_new_refresh_token(user_id: str, device_id: str, token: str):
    run_sql(
        """
        INSERT INTO refresh_tokens (user_id, device_id, refresh_token)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            refresh_token = VALUES(refresh_token)""",
        (user_id, device_id, token)
    )

def delete_refresh_token(user_id: str, device_id: str):
    run_sql(
        "UPDATE refresh_tokens SET refresh_token = %s WHERE user_id = %s AND device_id = %s",
        ("refresh_token", user_id, device_id)
    )

