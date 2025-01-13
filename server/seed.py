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

# Predefined data
categories = [
    "Groceries", "Transport", "Utilities", "Entertainment", "Healthcare",
    "Education", "Savings", "Dining Out", "Shopping", "Miscellaneous"
]

budget_names = [
    "Monthly Essentials", "Travel Fund", "Emergency Savings", "Home Renovation", 
    "Healthcare Expenses", "Debt Payoff Plan", "First Home Purchase"
]

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
            description=fake.sentence(nb_words=8),
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
            end_date = start_date + timedelta(days=30)  # End date should be 30 days after start date

            # Generate fake data
            name = fake.word() + " Budget"  # Generate a random word and append "Budget"
            description = fake.sentence(nb_words=6)  # Generate a random sentence
            total_amount = float(round(fake.random_number(digits=3), 2))  # Ensure this is a float
            budget_type = choice(['monthly', 'overall'])  # Randomly choose 'monthly' or 'overall'

            budget = Budget(
                name=name,
                description=description,
                total_amount=total_amount,  # Pass the float here
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
            description=fake.sentence(nb_words=5),
            amount=round(uniform(10.0, 500.0), 2),  # Random amount between 10 and 500
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
        # Ensure the expense is valid and has an ID
        if not expense or not expense.id:
            print(f"Invalid expense: {expense}")  # Debugging line
            raise ValueError(f"Expense with ID {expense.id} does not exist.")
        
        print(f"Seeding transaction for Expense ID: {expense.id}")  # Debugging line

        # Randomize the transaction type between 'debit' and 'credit'
        transaction_type = choice(['debit', 'credit'])
        
        # Generate a random transaction amount (for example between 5 and 200)
        transaction_amount = round(uniform(5.0, 200.0), 2)

        # Create a transaction linked to the valid expense
        transaction = Transaction(
            transaction_type=transaction_type,  # Randomized between 'debit' and 'credit'
            amount=transaction_amount,  # Randomized amount
            date=fake.date_this_year(before_today=True),  # Random transaction date
            expense_id=expense.id  # Ensure that expense_id is set correctly
        )
        
        db.session.add(transaction)
        
    db.session.commit()

def seed_savings(users):
    savings = []  # Initialize a list to store the saving objects

    current_year = datetime.now().year  # Get the current year

    for user in users:
        # Dynamically set month and year, ensuring the year is current or future
        month = random.randint(1, 12)  # Random month between 1 and 12
        year = random.choice([current_year, current_year + 1])  # Choose either the current year or the next year

        # Generate random goal amount and current savings
        goal_amount = round(random.uniform(1000.00, 10000.00), 2)  # Goal between $1,000 and $10,000
        current_savings = round(random.uniform(0.00, goal_amount), 2)  # Current savings between 0 and goal amount
        
        # Ensure goal_amount and current_savings are Decimal
        goal_amount = Decimal(str(goal_amount))
        current_savings = Decimal(str(current_savings))
        
        # Check that month is an integer
        if not isinstance(month, int):
            raise TypeError(f"Invalid month: {month}, it must be an integer.")
        
        # Create Saving object with valid month, year, goal_amount, and current_savings
        saving = Saving(
            user_id=user.id,
            month=month,  # Ensure this is an integer
            year=year,    # Ensure this is an integer
            goal_amount=goal_amount,  # Ensure it's a Decimal
            current_savings=current_savings  # Ensure it's a Decimal
        )
        
        # Add the saving object to the list
        savings.append(saving)
        
        # Add the saving object to the session
        db.session.add(saving)
    
    # Commit the session to persist the data
    db.session.commit()

    return savings  # Return the list of savings

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
