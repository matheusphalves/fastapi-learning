from pydantic import BaseModel


class FinancialExpenseBase(BaseModel):
    financial_user_id: int
    type: str
    description: str


class FinancialExpenseUpdateRequest(BaseModel):
    id: int
    financial_user_id: int
    type: str
    description: str


class FinancialExpenseRequest(FinancialExpenseBase):
    pass


class FinancialExpenseResponse(FinancialExpenseBase):
    id: int

    class Config:
        orm_mode = True
