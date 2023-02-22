from pydantic import BaseModel


class FinancialExpenseEntry(BaseModel):
    financial_expense_id: int
    amount: float
    description: str


class FinancialExpenseRequest(FinancialExpenseEntry):
    pass


class FinancialExpenseResponse(FinancialExpenseEntry):
    id: int

    class Config:
        orm_mode = True
