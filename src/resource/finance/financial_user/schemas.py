from typing import List

from pydantic import BaseModel

from src.database.models import FinancialExpense


class FinancialUserBase(BaseModel):
    firstName: str
    lastName: str
    login: str
    password: str


class FinancialUserUpdateRequest(BaseModel):
    id: int
    firstName: str
    lastName: str
    login: str
    password: str


class FinancialUserRequest(FinancialUserBase):
    pass


class FinancialUserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str

    class Config:
        orm_mode = True


class FinancialUserLogin(BaseModel):
    login: str
    password: str
