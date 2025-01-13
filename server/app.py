from werkzeug.exceptions import NotFound
from config import app, api

# User Folder Route
from routes.user.login import Login
from routes.user.currentuser import CurrentUser
from routes.user.currentuser import CurrentUserPatch
from routes.user.currentuser import UserDelete
from routes.user.googlesignin import GoogleAuth
from routes.user.logout import Logout
# from routes.user.recoverpassword import
from routes.user.refresh import Refresh
from routes.user.signup import Signup

# Budget Folder Route
from routes.budget.budgetdelete import BudgetsDelete
from routes.budget.budgetsbyid import BudgetsById
from routes.budget.budgetsget import BudgetsGet
from routes.budget.budgetspatch import BudgetPatch 
from routes.budget.budgetspost import BudgetPost

# Expense Folder Route
from routes.expense.expensebyid import ExpensesById
from routes.expense.expensedelete import ExpensesDelete
from routes.expense.expenseget import ExpensesGet
from routes.expense.expensepatch import ExpensesPatch
from routes.expense.expensepost import ExpensesPost

# Category Folder Route
from routes.category.categorybyid import CategoriesById
from routes.category.categorydelete import CategoriesDelete
from routes.category.categoryget import CategoriesGet
from routes.category.categorypatch import CategoriesPatch
from routes.category.categorypost import CategoriesPost

# Saving Folder Route
from routes.savings.savingsbyid import SavingsById
from routes.savings.savingsdelete import SavingsDelete
from routes.savings.savingsget import SavingsGet
from routes.savings.savingspatch import SavingsPatch
from routes.savings.savingspost import SavingsPost

# Transaction Folder Route
from routes.transaction.transactionbyid import TransactionById
from routes.transaction.transactiondelete import TransactionDelete
from routes.transaction.transactionget import TransactionsGet
from routes.transaction.transactionpatch import TransactionPatch
from routes.transaction.transactionpost import TransactionsPost

# BudegtCategories
# from routes.budgetcategory.budcatdelete import DeleteBudgetCategory
from routes.budgetcategory.budcatget import GetCategoriesForBudget
# from routes.budgetcategory.budcatpost import AddBudgetCategory



# API Routes

@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


# User Api Routes
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CurrentUser, "/current-user")
api.add_resource(CurrentUserPatch, "/current-user/update")
api.add_resource(Logout, "/logout")
api.add_resource(Refresh, "/refresh")
api.add_resource(UserDelete, "/delete-account")
api.add_resource(GoogleAuth, "/google-auth")
# api.add_resource(Recoverpassword, "/recover-password")
# api.add_resource(ResetPassword, "/reset-password")

# Budget Api Route
api.add_resource(BudgetPost, "/budgets/create")
api.add_resource(BudgetsGet, "/budgets")  
api.add_resource(BudgetsById, "/budgets/<int:budget_id>")
api.add_resource(BudgetPatch, "/budgets/<int:budget_id>/update") 
api.add_resource(BudgetsDelete, "/budgets/<int:budget_id>/delete") 

# Expense Api Route
api.add_resource(ExpensesPost, "/expenses/create")
api.add_resource(ExpensesGet, "/expenses")  
api.add_resource(ExpensesById, "/expenses/<int:expense_id>")  
api.add_resource(ExpensesPatch, "/expenses/<int:expense_id>/update") 
api.add_resource(ExpensesDelete, "/expenses/<int:expense_id>/delete") 

# Category Api Route
api.add_resource(CategoriesPost, "/categories/create")
api.add_resource(CategoriesGet, "/categories")  
api.add_resource(CategoriesById, "/categories/<int:category_id>")
api.add_resource(CategoriesPatch, "/categories/<int:category_id>/update") 
api.add_resource(CategoriesDelete, "/categories/<int:category_id>/delete") 

# Budget Categories Api Route
api.add_resource(GetCategoriesForBudget, "/budget-category")

# Transaction Api Route
api.add_resource(TransactionsGet, "/transactions")
api.add_resource(TransactionsPost, "/transactions/create")
api.add_resource(TransactionById, "/transactions/<int:transaction_id>")
api.add_resource(TransactionPatch, "/transactions/<int:transaction_id>/update")
api.add_resource(TransactionDelete, "/transactions/<int:transaction_id>/delete")

# Saving Api Route
api.add_resource(SavingsGet, "/savings")
api.add_resource(SavingsPost, "/savings/create")
api.add_resource(SavingsById, "/savings/<int:savings_id>")
api.add_resource(SavingsPatch, "/savings/<int:savings_id>/update")
api.add_resource(SavingsDelete, "/savings/<int:savings_id>/delete")




if __name__ == '__main__':
    app.run(port=5555, debug=True)

