class Budget:
    def __init__(self, budget_id: int, group_id: int, budget_name: str, total_budget: int, created_date=None, last_updated=None):
        self.budget_id = budget_id
        self.group_id = group_id
        self.budget_name = budget_name
        self.total_budget = total_budget
        

    @staticmethod
    def get_all_budgets_by_group(cursor, group_id):
        query = "SELECT * FROM budget WHERE group_id = %s"
        cursor.execute(query, (group_id,))
        result = cursor.fetchall()
        return [{'budget_id': budget[0], 'budget_name': budget[2], 'total_budget': budget[3]} for budget in result]

    
    @staticmethod
    def get_budget_name_by_id(cursor, budget_id):
        query = "SELECT budget_name, total_budget FROM budget WHERE budget_id = %s"
        cursor.execute(query, (budget_id,))
        return cursor.fetchone()


    @staticmethod
    def add_budget(cursor, group_id, budget_name, total_budget):
        query = "INSERT INTO budget (group_id, budget_name, total_budget) VALUES (%s, %s, %s)"
        cursor.execute(query, (group_id, budget_name, total_budget))


    @staticmethod
    def update_budget(cursor, budget_id, budget_name=None, total_budget=None):
        query = "UPDATE budget SET budget_name = %s, total_budget = %s WHERE budget_id = %s"
        params = [budget_name, total_budget, budget_id]

        cursor.execute(query, tuple(params))


    @staticmethod
    def delete_budget(cursor, budget_id):
        query = "DELETE FROM budget WHERE budget_id = %s"
        cursor.execute(query, (budget_id,))
