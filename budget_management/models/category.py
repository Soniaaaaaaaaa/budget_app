class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name


    @staticmethod
    def get_all_categories(cursor):
        query = "SELECT category_id, category_name FROM category"
        cursor.execute(query)
        result = cursor.fetchall() 
        return result
