from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.core.security.auth import create_access_token
from src.core.security.security import get_password_hash, verify_password
from src.database.database import database_conector
from src.database.models import FinancialUser, FinancialExpense
from src.resource.finance.financial_expense.schemas import FinancialExpenseResponse
from src.resource.finance.financial_user.repository import FinancialUserRepository
from src.resource.finance.financial_user.schemas import FinancialUserResponse, FinancialUserRequest, \
    FinancialUserUpdateRequest, FinancialUserLogin, FinancialUserLoginResponse

financial_users_router = APIRouter(prefix="/api/financial-users", tags=["Financial Users"])

financial_user_repository = FinancialUserRepository()


@financial_users_router.post(path="", response_model=FinancialUserResponse, status_code=status.HTTP_201_CREATED)
async def create(request: FinancialUserRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_user_request = FinancialUser(**request.dict())
    financial_user_request.password = get_password_hash(financial_user_request.password)
    financial_user = financial_user_repository.save(db, financial_user_request)
    return FinancialUserResponse.from_orm(financial_user)


@financial_users_router.put(path="", response_model=FinancialUserResponse, status_code=status.HTTP_200_OK)
async def update(request: FinancialUserUpdateRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_user_request = FinancialUser(**request.dict())
    financial_user_request.password = get_password_hash(financial_user_request.password)
    financial_user = financial_user_repository.update(db, financial_user_request)

    if financial_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialUserResponse.from_orm(financial_user)


@financial_users_router.get(path="", response_model=List[FinancialUserResponse])
async def find_all(db: Session = Depends(database_conector.get_database_session)):
    financial_users = financial_user_repository.find_all(db)
    return [FinancialUserResponse.from_orm(financialUser) for financialUser in financial_users]


@financial_users_router.delete(path="/{financial_user_id}")
async def delete(financial_user_id: int, db: Session = Depends(database_conector.get_database_session)):
    financial_user_repository.delete_by_id(db, financial_user_id)


@financial_users_router.get(path="/{financial_user_id}/financial-expenses")
async def get_financial_expenses_by_user(financial_user_id: int,
                                         db: Session = Depends(database_conector.get_database_session)):
    financial_expenses = financial_user_repository.get_related_entries(db, financial_user_id, FinancialExpense,
                                                                       "financial_user_id")
    return [FinancialExpenseResponse.from_orm(financial_expense) for financial_expense in financial_expenses]


@financial_users_router.post(path="/token", status_code=status.HTTP_200_OK)
async def generate_auth_token(request: FinancialUserLogin, db: Session = Depends(database_conector.get_database_session)):

    financial_user = financial_user_repository.get_user_by_login(db, request.login)

    if financial_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    if not verify_password(request.password, financial_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


    return {"access_token": create_access_token({"sub": financial_user.login})}


