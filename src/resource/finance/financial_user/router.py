from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database.database import database_conector
from src.database.models import FinancialUser
from src.resource.finance.financial_user.repository import FinancialUserRepository
from src.resource.finance.financial_user.schemas import FinancialUserResponse, FinancialUserRequest, \
    FinancialUserUpdateRequest

financial_users_router = APIRouter(prefix="/api/financial-users", tags=["Financial Users"])

financial_user_repository = FinancialUserRepository()


@financial_users_router.post(path="", response_model=FinancialUserResponse, status_code=status.HTTP_201_CREATED)
async def create(request: FinancialUserRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_user = financial_user_repository.save(db, FinancialUser(**request.dict()))
    return FinancialUserResponse.from_orm(financial_user)


@financial_users_router.put(path="", response_model=FinancialUserResponse, status_code=status.HTTP_200_OK)
async def update(request: FinancialUserUpdateRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_user = financial_user_repository.update(db, FinancialUser(**request.dict()))
    if financial_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialUserResponse.from_orm(financial_user)


@financial_users_router.get(path="", response_model=List[FinancialUserResponse])
async def find_all(db: Session = Depends(database_conector.get_database_session)):
    financial_users = financial_user_repository.find_all(db)
    return [FinancialUserResponse.from_orm(financialUser) for financialUser in financial_users]


@financial_users_router.delete(path="/{financial_user_id}")
def delete(financial_user_id: int, db: Session = Depends(database_conector.get_database_session)):
    financial_user_repository.delete_by_id(db, financial_user_id)
