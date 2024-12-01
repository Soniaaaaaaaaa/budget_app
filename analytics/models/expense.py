class Expense:
	def __init__(self, expense_id: int, budget_id: int, description: str | None, amount: float, category_id: int, user_id: int):
		self.expense_id = expense_id
		self.budget_id = budget_id
		self.description = description
		self.amount = amount
		self.category_id = category_id
		self.user_id = user_id