class Expense:
    def __init__(self, expense_id: int, budget_id: int, description: str, price: float, amount: int, expense_type: str, category_id: int, created_date=None):
        self.expense_id = expense_id
        self.budget_id = budget_id
        self.description = description
        self.price = price
        self.expense_type = expense_type
        self.category_id = category_id
        self.created_date = created_date


    @staticmethod
    def get_all_expenses_by_budget(cursor, budget_id):
        query = "SELECT * FROM expense WHERE budget_id = %s ORDER BY created_date DESC"
        cursor.execute(query, (budget_id,))
        result = cursor.fetchall()
        return [{
            'expense_id': expense[0], 
            'description': expense[2], 
            'price': int(expense[3]), 
            'expense_type': expense[4],
            'category_id': expense[5],
            'created_date': expense[6]
        } for expense in result]


    @staticmethod
    def sum_current_expenses_this_month(cursor, budget_id):
        query = """
            SELECT sum(price)
            FROM expense
            WHERE budget_id = %s
            AND MONTH(created_date) = MONTH(CURRENT_DATE())
            AND YEAR(created_date) = YEAR(CURRENT_DATE())
            AND expense_type = 'current'
        """
        cursor.execute(query, (budget_id,))

        return cursor.fetchone()[0]


    @staticmethod
    def add_expense(cursor, budget_id, description, price, expense_type, category_id):
        query = """
        INSERT INTO expense (budget_id, description, price, expense_type, category_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (budget_id, description, price, expense_type, category_id))


    @staticmethod
    def update_expense(cursor, expense_id, description, price, expense_type, category_id):
        query = "UPDATE expense SET description = %s, price = %s, expense_type = %s, category_id = %s WHERE expense_id = %s"
        params = [description, price, expense_type, category_id, expense_id]

        cursor.execute(query, tuple(params))


    @staticmethod
    def delete_expense(cursor, expense_id):
        query = "DELETE FROM expense WHERE expense_id = %s"
        cursor.execute(query, (expense_id,))
