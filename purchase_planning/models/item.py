"""
This script describes the class for the item of the app

Item Blueprint has id as the primary key, name, description and assigned group
Item has id as the primary key, Item Blueprint, price, additional information and assigned purchase plan

Item Blueprint can only belong to one group
Item can only belong to one Purchase Plan
"""

from models.group import Group
from models.semantic_search import SemanticSearch

class ItemBlueprint:
    def __init__(self, item_blueprint_id: int, name: str, description: str):
        self.id = item_blueprint_id
        self.name = name
        self.description = description

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

    @staticmethod
    def get_item_blueprint_by_its_id(cursor, item_blueprint_id):
        cols = ["item_blp_id", "name", "description"]
        query = "SELECT item_blp_id, name, description FROM item_blueprint WHERE item_blp_id = %s"
        cursor.execute(query, (item_blueprint_id,))
        result = cursor.fetchone()
        if result is not None:
            result = {col: val for col, val in zip(cols, result)}
            item_blp_id = result["item_blp_id"]
            name = result["name"]
            description = result["description"]
            item_blueprint = ItemBlueprint(item_blp_id, name, description)
            return item_blueprint
        
    @staticmethod
    def add_item_blueprint(cursor, connection, name: str, description: str, group: Group) -> int:
        try:
            model = SemanticSearch(group.id)
            item_blp_id = model.find_similar(f'{name} ({description})')
            if item_blp_id is None:
                query = 'INSERT INTO item_blueprint (name, description, group_id) VALUES (%s, %s, %s)'
                cursor.execute(query, (name, description, group.id))
                connection.commit()
                query = 'SELECT item_blp_id FROM item_blueprint WHERE name = %s AND group_id = %s'
                cursor.execute(query, (name, group.id))
                result = cursor.fetchone()
                item_blp_id = int(result[0])
                model.add_new_point(item_blp_id, f'{name} ({description})')
            return item_blp_id
        except Exception as e:
            print(f'Something went wring here! {e}')
            return None

class Item:
    def __init__(self, item_id: int, additional_info: str, price: float, item_blueprint: ItemBlueprint):
        self.id = item_id
        self.additional_info = additional_info
        self.price = price
        self.item_blueprint = item_blueprint

    def __eq__(self, other):
        return self.id == other.id and self.item_blueprint == other.item_blueprint
    
    def __ne__(self, other):
        return self.id != other.id or self.item_blueprint != other.item_blueprint

    @staticmethod
    def get_items_by_plan_id(cursor, plan_id):
        cols = ["item_id", "item_blp_id", "add_info", "price"]
        query = "SELECT item_id, item_blp_id, add_info, price FROM item WHERE list_id = %s"
        cursor.execute(query, (plan_id,))
        result = cursor.fetchall()
        items = []
        for row in result:
            row = {col: val for col, val in zip(cols, row)}
            item_id = int(row["item_id"])
            item_blp_id = int(row["item_blp_id"])
            add_info = row["add_info"]
            price = float(row["price"])
            item_blueprint = ItemBlueprint.get_item_blueprint_by_its_id(cursor, item_blp_id)
            item = Item(item_id, add_info, price, item_blueprint)
            items.append(item)
        return items
