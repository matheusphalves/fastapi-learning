from fastapi import FastAPI

from src.resource.finance.financial_expense.router import financial_expenses_router
from src.resource.finance.financial_expense_entry.router import financial_expense_entries_router
from src.resource.finance.financial_user.router import financial_users_router

app = FastAPI()

app.include_router(financial_users_router)
app.include_router(financial_expenses_router)
app.include_router(financial_expense_entries_router)


@app.get("/")
async def root():
    return {"message": "Hello world!"}
