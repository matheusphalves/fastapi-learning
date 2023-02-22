from pydantic import BaseModel


class FinancialExpenseEntry(BaseModel):
    financial_expense_id: int
    amount: float
    description: str


class FinancialExpenseEntryUpdateRequest(BaseModel):
    id: int
    financial_expense_id: int
    amount: float
    description: str


class FinancialExpenseEntryRequest(FinancialExpenseEntry):
    pass


class FinancialExpenseEntryResponse(FinancialExpenseEntry):
    id: int

    class Config:
        orm_mode = True
