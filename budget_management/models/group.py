class Group:
    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name


    @staticmethod
    def get_group_name_by_id(cursor, group_id):
        query = "SELECT group_name FROM group_info WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        result = cursor.fetchone()
        return result[0] if result else None
