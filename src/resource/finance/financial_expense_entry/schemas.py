from datetime import datetime

from pydantic import BaseModel


class FinancialExpenseEntry(BaseModel):
    financial_expense_id: int
    amount: float
    description: str
    expense_date: datetime


class FinancialExpenseEntryUpdateRequest(FinancialExpenseEntry):
    id: int


class FinancialExpenseEntryRequest(FinancialExpenseEntry):
    pass


class FinancialExpenseEntryResponse(FinancialExpenseEntry):
    id: int

    class Config:
        orm_mode = True
