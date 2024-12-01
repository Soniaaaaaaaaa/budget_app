class Budget:
	def __init__(self, budget_id: int, family_id: int, total_budget: float, current_expenses: float, planned_expenses: float):
		self.budget_id = budget_id
		self.family_id = family_id
		self.total_budget = total_budget
		self.current_expenses = current_expenses
		self.planned_expenses = planned_expenses

		