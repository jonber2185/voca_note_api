from db.mySQL import run_sql

def search_set(title):
    if not title: return []
    result = run_sql(
        "SELECT * FROM sets WHERE title LIKE %s ORDER BY created_at DESC LIMIT 20",
        (f"%{title}%",),
    )
    if result is None: return []
    else: return result


def get_user_sets(user_id) -> list:
    result = run_sql(
        "SELECT * FROM sets WHERE owner_id = %s ORDER BY created_at DESC",
        (user_id,),
    )
    if result is None: return []
    else: return result

def get_user_set(set_id, user_id):
    result = run_sql(
        "SELECT * FROM sets WHERE id = %s AND owner_id = %s",
        (set_id, user_id),
        fetchone=True
    )
    if result is None: return {}
    else: return result

def create_set(set_id, title, description, owner_id, is_public):
    run_sql(
        "INSERT INTO sets (id, title, description, owner_id, is_public) VALUES (%s, %s, %s, %s, %s)",
        (set_id, title, description, owner_id, is_public),
    )

def update_set(set_id, owner_id, title, description, is_public):
    run_sql(
        """
        UPDATE sets 
        SET title = COALESCE(%s, title),
            description = COALESCE(%s, description),
            is_public = COALESCE(%s, is_public)
        WHERE id = %s AND owner_id = %s
        """,
        (title, description, is_public, set_id, owner_id),
    )
    
def delete_set(set_id, owner_id):
    run_sql(
        "DELETE FROM sets WHERE id = %s AND owner_id = %s",
        (set_id, owner_id)
    )
    