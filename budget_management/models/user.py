class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password


    @staticmethod
    def get_username_by_id(cursor, user_id):
        query = "SELECT username FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
