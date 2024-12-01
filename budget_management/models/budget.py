class Budget:
    def __init__(self, budget_id: int, group_id: int, budget_name: str, total_budget: int, created_date=None, last_updated=None):
        self.budget_id = budget_id
        self.group_id = group_id
        self.budget_name = budget_name
        self.total_budget = total_budget
        self.created_date = created_date
        self.last_updated = last_updated


    @staticmethod
    def get_all_budgets_by_group(cursor, group_id):
        query = "SELECT * FROM budget WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        return [Budget(*row) for row in cursor.fetchall()]


    @staticmethod
    def get_budget_by_id(cursor, budget_id):
        query = "SELECT * FROM budget WHERE budget_id = %s"
        cursor.execute(query, (budget_id,))
        result = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description] 
        return dict(zip(columns, result))


    @staticmethod
    def add_budget(cursor, group_id, budget_name, total_budget):
        query = "INSERT INTO budget (group_id, budget_name, total_budget) VALUES (%s, %s, %s)"
        cursor.execute(query, (group_id, budget_name, total_budget))


    @staticmethod
    def update_budget(cursor, budget_id, budget_name=None, total_budget=None):
        query = "UPDATE budget SET"
        params = []
        if budget_name:
            query += " budget_name = %s,"
            params.append(budget_name)
        if total_budget:
            query += " total_budget = %s,"
            params.append(total_budget)
        
        query += " last_updated = CURRENT_TIMESTAMP WHERE budget_id = %s"
        params.append(budget_id)

        cursor.execute(query, tuple(params))


    @staticmethod
    def delete_budget(cursor, budget_id):
        query = "DELETE FROM budget WHERE budget_id = %s"
        cursor.execute(query, (budget_id,))
