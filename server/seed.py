#!/usr/bin/env python3

# Remote library imports
from faker import Faker
from random import randint, uniform, choice
import random
from datetime import datetime, timedelta, date
from decimal import Decimal

# Local imports
from app import app
from config import db
from models.user import User
from models.category import Category
from models.budget import Budget
from models.expense import Expense
from models.saving import Saving
from models.transaction import Transaction
from models.budgetcategories import BudgetCategories

fake = Faker()

categories = [
    "Groceries", "Transport", "Utilities", "Entertainment", "Healthcare",
    "Education", "Savings", "Dining Out", "Shopping", "Miscellaneous"
]

budget_names = [
    "Monthly Essentials", "Travel Fund", "Emergency Savings", "Home Renovation", 
    "Healthcare Expenses", "Debt Payoff Plan", "First Home Purchase"
]

budget_description_map = {
    "Monthly Essentials": "Manage essential living expenses like rent, utilities, and food.",
    "Travel Fund": "Set aside funds for upcoming travel expenses and adventures.",
    "Emergency Savings": "Ensure financial security with an emergency savings plan.",
    "Home Renovation": "Save for future home renovations and improvements.",
    "Healthcare Expenses": "Plan ahead for unexpected medical costs and emergencies.",
    "Debt Payoff Plan": "Prioritize paying off outstanding debts efficiently.",
    "First Home Purchase": "Plan for large purchases by setting specific savings goals.",
}

expense_description_map = {
    "Monthly Essentials": ["Groceries", "Rent payment", "Utility bill", "Internet bill", "Phone bill"],
    "Travel Fund": ["Flight ticket", "Hotel stay", "Car rental", "Tour package", "Travel insurance"],
    "Emergency Savings": ["Unexpected medical bill", "Car repair", "Home emergency repair", "Vet bill"],
    "Home Renovation": ["New furniture", "Kitchen upgrade", "Bathroom renovation", "Painting walls"],
    "Healthcare Expenses": ["Doctor visit", "Prescription medication", "Health insurance", "Physical therapy"],
    "Debt Payoff Plan": ["Credit card payment", "Loan repayment", "Student loan installment"],
    "First Home Purchase": ["Down payment", "Mortgage payment", "Property tax", "Home inspection"],
}


def seed_users(num_users=10): 
    users = []
    for _ in range(num_users):
        user = User(name=fake.name(), email=fake.email())
        user.password = ("Password11!!") 
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users

def seed_categories():
    category_objects = []
    for category_name in categories:
        category = Category(
            name=category_name,
            description=choice(categories),
            is_default=True,
            created_at=fake.date_time_this_year(before_now=True),
            updated_at=fake.date_time_this_year(before_now=True),
        )
        db.session.add(category)
        category_objects.append(category)
    db.session.commit()
    return category_objects

def seed_budgets(users, categories):
    budgets = []
    for user in users:
        for category in categories:
            start_date = date.today()
            end_date = start_date + timedelta(days=30) 
            name = choice(budget_names)
            description = budget_description_map.get(name, "Plan your finances wisely.")
            total_amount = float(round(fake.random_number(digits=3), 2)) 
            budget_type = choice(['monthly', 'overall']) 

            budget = Budget(
                name=name,
                description=description,
                total_amount=total_amount,
                start_date=start_date,
                end_date=end_date,
                user_id=user.id,
                category_id=category.id,
                budget_type=budget_type
            )
            db.session.add(budget)
            budgets.append(budget)

    db.session.commit()
    return budgets

def seed_budget_categories(budgets, categories):
    for budget in budgets:
        associated_categories = fake.random_elements(elements=categories, length=randint(1, 3), unique=True)
        for category in associated_categories:
            budget_category = BudgetCategories(
                budget_id=budget.id,
                category_id=category.id,
            )
            db.session.add(budget_category)
    db.session.commit()

def seed_expenses(budgets, num_expenses=50):
    expenses = []
    for _ in range(num_expenses):
        budget = choice(budgets)
        expense = Expense(
            description = choice(expense_description_map.get(budget.name, ["Miscellaneous expense"])),
            amount=round(uniform(10.0, 500.0), 2),  
            date=fake.date_this_year(before_today=True),
            budget_id=budget.id,
            created_at=fake.date_time_this_year(before_now=True),
            updated_at=fake.date_time_this_year(before_now=True),
        )
        db.session.add(expense)
        expenses.append(expense)
    db.session.commit()
    return expenses

def seed_transactions(expenses):
    for expense in expenses:
        if not expense or not expense.id:
            print(f"Invalid expense: {expense}")  
            raise ValueError(f"Expense with ID {expense.id} does not exist.")
        print(f"Seeding transaction for Expense ID: {expense.id}")  
        transaction_type = choice(['debit', 'credit'])
        transaction_amount = round(uniform(5.0, 200.0), 2)
        transaction = Transaction(
            transaction_type=transaction_type, 
            amount=transaction_amount, 
            date=fake.date_this_year(before_today=True),
            expense_id=expense.id
        )
        
        db.session.add(transaction)
    db.session.commit()

def seed_savings(users):
    savings = [] 

    current_year = datetime.now().year 

    for user in users:
        month = random.randint(1, 12) 
        year = random.choice([current_year, current_year + 1]) 
        goal_amount = round(random.uniform(1000.00, 10000.00), 2) 
        current_savings = round(random.uniform(0.00, goal_amount), 2)
        goal_amount = Decimal(str(goal_amount))
        current_savings = Decimal(str(current_savings))
        if not isinstance(month, int):
            raise TypeError(f"Invalid month: {month}, it must be an integer.")
        saving = Saving(
            user_id=user.id,
            month=month,
            year=year,
            goal_amount=goal_amount,
            current_savings=current_savings 
        )
        savings.append(saving)
        db.session.add(saving)
    db.session.commit()
    return savings

def run_seeds():
    print("Seeding database...")
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = seed_users()
        print(f"Seeded {len(users)} users.")

        categories = seed_categories()
        print(f"Seeded {len(categories)} categories.")

        budgets = seed_budgets(users, categories)
        print(f"Seeded {len(budgets)} budgets.")

        seed_budget_categories(budgets, categories)
        print(f"Linked budgets with categories.")

        expenses = seed_expenses(budgets)
        print(f"Seeded {len(expenses)} expenses.")

        seed_transactions(expenses)
        print(f"Seeded transactions for expenses.")

        savings = seed_savings(users)
        print(f"Seeded {len(savings)} savings.")

    print("Seeding completed!")

if __name__ == "__main__":
    run_seeds()
