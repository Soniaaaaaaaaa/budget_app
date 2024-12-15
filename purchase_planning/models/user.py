"""
This script describes the class for the user of the app

User has id as the primary key, name and email
"""

from models.group import Group

class User:
    def __init__(self, user_id: int, name: str, email: str, group: Group):
        self.id = user_id
        self.name = name
        self.email = email
        self.group = group

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

    @staticmethod
    def get_user_by_id(cursor, user_id: int):
        cols = ["user_id", "username", "email", "group_id"]
        query = "SELECT user_id, username, email, group_id FROM user WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result is not None:
            result = {col: val for col, val in zip(cols, result)}
            user_id = int(result["user_id"])
            username = result["username"]
            email = result["email"]
            group_id = result["group_id"]
            group = Group.get_group_by_id(cursor, group_id)
            if group is None:
                return None
            user = User(user_id, username, email, group)
            return user
        return None