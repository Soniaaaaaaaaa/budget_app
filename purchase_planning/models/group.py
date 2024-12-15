"""
This script describes the class for the user group of the app

Group has id as the primary key and name
"""
from datetime import datetime, timedelta

class Group:
    def __init__(self, group_id: int, name: str):
        self.id = group_id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

    @staticmethod
    def get_group_by_id(cursor, group_id: int):
        cols = ["group_id", "group_name"]
        query = "SELECT group_id, group_name FROM group_info WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        result = cursor.fetchone()
        if result is not None:
            result = {col: val for col, val in zip(cols, result)}
            group_id = int(result["group_id"])
            group_name = result["group_name"]
            group = Group(group_id, group_name)
            return group
        return None
    
    @staticmethod
    def get_propositions(cursor, group_id: int):
        cols = ["group_id", "name", "description", "item_num", "last_purchase", "avg_period"]
        query = "SELECT * FROM proposition WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        result = cursor.fetchall()
        res = []
        today = datetime.now()
        for row in result:
            row = {col: val for col, val in zip(cols, row)}
            text = f"{row['name']} ({row['description']})"
            last_purchase: datetime= row["last_purchase"]
            next_purchase = last_purchase + timedelta(days=int(row['avg_period']))
            res.append([text, last_purchase.strftime('%d.%m.%Y'), next_purchase])
        res = sorted(res, key=lambda item: abs((item[-1] - today).days))
        return [f"{row[0]} - Last added on {row[1]}" for row in res]
