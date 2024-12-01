"""
This script describes the class for the user group of the app

Group has id as the primary key and name
"""

class Group:
    def __init__(self, group_id: int, name: str):
        self.id = group_id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

    @staticmethod
    def get_group_by_user_id(cursor, user_id: int):
        cols = ["group_id", "group_name"]
        query = "SELECT group_info.group_id, group_name FROM group_info JOIN member ON group_info.group_id = member.group_id WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result is not None:
            result = {col: val for col, val in zip(cols, result)}
            group_id = int(result["group_id"])
            group_name = result["group_name"]
            group = Group(group_id, group_name)
            return group
        return None
