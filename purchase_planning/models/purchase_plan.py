"""
This script describes the class for the purchase plan of the app

Purchase Plan has id as the primary key, name, assigned group and balance

Purchase Plan can only belong to one group
"""

from models.group import Group
from models.item import Item, ItemBlueprint
from models.user import User
from datetime import date

class PurchasePlan:
    def __init__(self, plan_id: int, name: str, group: Group, balance: float, cursor):
        self.id = plan_id
        self.name = name
        self.group = group
        self.balance = balance
        self.items = Item.get_items_by_plan_id(cursor, plan_id)

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id
    
    def add_item(self, cursor, connection, name: str, description: str, add_info: str, price: float, user: User) -> int:
        try:
            if user.group != self.group:
                return 3
            """
            if item in self.items:
                return 2
            """
            if self.balance < price:
                return 4
            self.balance -= price
            PurchasePlan.insert_item(cursor, connection, name, description, add_info, price, self, user)
            PurchasePlan.update_purchse_plan(cursor, connection, self.id, self.balance)
            self.items = Item.get_items_by_plan_id(cursor, self.id)
            return 1
        except:
            return 0
        
    def remove_item(self, cursor, connection, item_id: int, user: User) -> int:
        try:
            if user.group != self.group:
                return 3
            """
            if item not in self.items:
                return 2
            """
            price = PurchasePlan.get_item_price(cursor, item_id, self.id)
            if price is None:
                return 2
            self.balance += price
            PurchasePlan.delete_item(cursor, connection, item_id)
            PurchasePlan.update_purchse_plan(cursor, connection, self.id, self.balance)
            self.items = Item.get_items_by_plan_id(cursor, self.id)
            return 1
        except:
            return 0

    @staticmethod
    def get_purchase_plan_by_id(cursor, group: Group, plan_id: int):
        cols = ["list_id", "list_name", "balance"]
        query = "SELECT list_id, list_name, balance FROM shopping_list WHERE list_id = %s AND group_id = %s"
        cursor.execute(query, (plan_id, group.id))
        result = cursor.fetchone()
        if result is not None:
            result = {col: val for col, val in zip(cols, result)}
            plan_id = result["list_id"]
            name = result["list_name"]
            balance = result["balance"]
            purchase_plan = PurchasePlan(plan_id, name, group, balance, cursor)
            return purchase_plan
        return None

    @staticmethod
    def get_purchase_plans_by_group(cursor, group: Group):
        cols = ["list_id", "list_name", "balance"]
        query = "SELECT list_id, list_name, balance FROM shopping_list WHERE group_id = %s"
        cursor.execute(query, (group.id,))
        result = cursor.fetchall()
        purchase_plans = []
        for row in result:
            row = {col: val for col, val in zip(cols, row)}
            plan_id = row["list_id"]
            name = row["list_name"]
            balance = row["balance"]
            purchase_plan = PurchasePlan(plan_id, name, group, balance, cursor)
            purchase_plans.append(purchase_plan)
        return purchase_plans

    @staticmethod
    def add_purchase_plan(cursor, connection, name: str, group: Group, balance: float) -> int:
        try:
            date_str = date.today().strftime('%Y-%m-%d')
            query = 'INSERT INTO shopping_list (group_id, list_name, balance, created_date, updated_date) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query, (group.id, name, balance, date_str, date_str))
            connection.commit()
            return 1
        except Exception as e:
            return 0

    @staticmethod
    def delete_purchase_plan(cursor, connection, plan_id: int):
        try:
            query = 'DELETE FROM item WHERE list_id = %s'
            cursor.execute(query, (plan_id, ))
            query = 'DELETE FROM shopping_list WHERE list_id = %s'
            cursor.execute(query, (plan_id, ))
            connection.commit()
            return 1
        except:
            return 0

    @staticmethod
    def insert_item(cursor, connection, name: str, description: str, add_info: str, price: float, purchase_plan, user: User) -> int:
        try:
            item_blp_id = ItemBlueprint.add_item_blueprint(cursor, connection, name, description, purchase_plan.group)
            query = 'INSERT INTO item (item_blp_id, add_info, price, creator_id, list_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query, (item_blp_id, add_info, price, user.id, purchase_plan.id))
            connection.commit()
            return 1
        except:
            return 0

    @staticmethod
    def delete_item(cursor, connection, item_id: int) -> int:
        try:
            query = 'DELETE FROM item WHERE item_id = %s'
            cursor.execute(query, (item_id,))
            connection.commit()
            return 1
        except:
            return 0

    @staticmethod
    def update_purchse_plan(cursor, connection, purchase_plan_id: int, balance: float):
        try:
            date_str = date.today().strftime('%Y-%m-%d')
            query = 'UPDATE shopping_list SET balance = %s, updated_date = "%s" WHERE list_id = %s'
            cursor.execute(query, (balance, date_str, purchase_plan_id))
            connection.commit()
            return 1
        except:
            return 0

    @staticmethod
    def get_item_price(cursor, item_id: int, purchase_plan_id: int):
        query = "SELECT price FROM item WHERE item_id = %s AND list_id = %s"
        cursor.execute(query, (item_id, purchase_plan_id))
        result = cursor.fetchone()
        return float(result[0]) if result else None

    @staticmethod
    def check_user_plan(cursor, user_id: int, purchase_plan_id: int) -> bool:
        query = "SELECT * FROM shopping_list JOIN member ON shopping_list.group_id AND member.group_id WHERE member.user_id = %s AND shopping_list.list_id = %s"
        cursor.execute(query, (user_id, purchase_plan_id))
        result = cursor.fetchone()
        return result is not None