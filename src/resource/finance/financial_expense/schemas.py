from pydantic import BaseModel


class FinancialExpenseBase(BaseModel):
    financial_user_id: int
    type: str
    description: str
    goal_amount: float


class FinancialExpenseUpdateRequest(FinancialExpenseBase):
    id: int


class FinancialExpenseRequest(FinancialExpenseBase):
    pass


class FinancialExpenseResponse(FinancialExpenseBase):
    id: int

    class Config:
        orm_mode = True
