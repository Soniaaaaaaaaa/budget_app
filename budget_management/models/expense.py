class Expense:
    def __init__(self, expense_id: int, budget_id: int, description: str, price: float, amount: int, expense_type: str, category_id: int, user_id: int, created_date=None):
        self.expense_id = expense_id
        self.budget_id = budget_id
        self.description = description
        self.price = price
        self.amount = amount
        self.expense_type = expense_type
        self.category_id = category_id
        self.user_id = user_id
        self.created_date = created_date


    @staticmethod
    def get_all_expenses_by_budget(cursor, budget_id):
        query = "SELECT * FROM expense WHERE budget_id = %s ORDER BY created_date DESC"
        cursor.execute(query, (budget_id,))
        return [Expense(*row) for row in cursor.fetchall()]

    
    @staticmethod
    def get_planned_by_budget(cursor, budget_id):
        query = "SELECT * FROM expense WHERE budget_id = %s AND expense_type = 'planned' ORDER BY created_date DESC"
        cursor.execute(query, (budget_id,))
        return [Expense(*row) for row in cursor.fetchall()]

    
    @staticmethod
    def get_current_by_budget(cursor, budget_id):
        query = "SELECT * FROM expense WHERE budget_id = %s AND expense_type = 'current' ORDER BY created_date DESC"
        cursor.execute(query, (budget_id,))
        return [Expense(*row) for row in cursor.fetchall()]


    @staticmethod
    def get_current_expenses_this_month(cursor, budget_id):
        query = """
            SELECT expense_id, budget_id, description, price, amount, category_id, expense_type, created_date
            FROM expense
            WHERE budget_id = %s
            AND MONTH(created_date) = MONTH(CURRENT_DATE())
            AND YEAR(created_date) = YEAR(CURRENT_DATE())
            AND expense_type = 'current'
            ORDER BY created_date DESC
        """
        cursor.execute(query, (budget_id,))

        return [Expense(*row) for row in cursor.fetchall()]


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
    def add_expense(cursor, budget_id, description, price, amount, expense_type, category_id, user_id):
        query = """
        INSERT INTO expense (budget_id, description, price, amount, expense_type, category_id, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if amount is None or amount == '':
            amount = 1
        cursor.execute(query, (budget_id, description, price, amount, expense_type, category_id, user_id))


    @staticmethod
    def update_expense(cursor, expense_id, description=None, price=None, amount=None, expense_type=None, category_id=None):
        query = "UPDATE expense SET"
        params = []
        
        if description:
            query += " description = %s,"
            params.append(description)
        if price is not None:
            query += " price = %s,"
            params.append(price)
        if amount is not None:
            query += " amount = %s,"
            params.append(amount)
        if expense_type:
            query += " expense_type = %s,"
            params.append(expense_type)
        if category_id:
            query += " category_id = %s,"
            params.append(category_id)
        
        # Обновление created_date
        query = query.rstrip(",") + "WHERE expense_id = %s"
        params.append(expense_id)

        cursor.execute(query, tuple(params))


    @staticmethod
    def delete_expense(cursor, expense_id):
        query = "DELETE FROM expense WHERE expense_id = %s"
        cursor.execute(query, (expense_id,))

    @staticmethod
    def get_expense_by_id(cursor, expense_id):
        query = "SELECT * FROM expense WHERE expense_id = %s"
        cursor.execute(query, (expense_id,))
        result = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description] 
        return dict(zip(columns, result))