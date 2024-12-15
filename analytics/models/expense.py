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
    def get_expenses_by_group(cursor, group_id):
        query = """
        SELECT e.expense_id, e.budget_id, e.description, e.price, e.expense_type, 
               e.created_date, e.category_id, c.category_name
        FROM expense e
        INNER JOIN budget b ON e.budget_id = b.budget_id
        LEFT JOIN category c ON e.category_id = c.category_id
        WHERE b.group_id = %s AND expense_type = 'current'
        """
        cursor.execute(query, (group_id,))
        result = cursor.fetchall()
        return [{
            'expense_id': expense[0], 
            'description': expense[2], 
            'price': int(expense[3]), 
            'expense_type': expense[4],
            'category_id': expense[6],
            'category_name': expense[7],
            'created_date': expense[5]
        } for expense in result]
