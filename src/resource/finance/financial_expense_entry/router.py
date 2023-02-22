from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import database_conector
from src.database.models import FinancialExpenseEntry
from src.resource.finance.financial_expense_entry.repository import FinancialExpenseEntryRepository
from src.resource.finance.financial_expense_entry.schemas import FinancialExpenseEntryResponse, \
    FinancialExpenseEntryRequest, FinancialExpenseEntryUpdateRequest

financial_expense_entries_router = APIRouter(prefix="/api/financial-expense-entries",
                                             tags=["Financial Expense Entries"])

financial_expense_entry_repository = FinancialExpenseEntryRepository()


@financial_expense_entries_router.post(path="", response_model=FinancialExpenseEntryResponse,
                                       status_code=status.HTTP_201_CREATED)
async def create(request: FinancialExpenseEntryRequest, db: Session = Depends(database_conector.get_database_session)):
    financial_expense_entry = financial_expense_entry_repository.save(db, FinancialExpenseEntry(**request.dict()))
    if financial_expense_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialExpenseEntryResponse.from_orm(financial_expense_entry)


@financial_expense_entries_router.put(path="", response_model=FinancialExpenseEntryResponse,
                                      status_code=status.HTTP_200_OK)
async def update(request: FinancialExpenseEntryUpdateRequest,
                 db: Session = Depends(database_conector.get_database_session)):
    financial_expense_entry = financial_expense_entry_repository.update(db, FinancialExpenseEntry(**request.dict()))
    if financial_expense_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FinancialExpenseEntryResponse.from_orm(financial_expense_entry)


@financial_expense_entries_router.get(path="", response_model=List[FinancialExpenseEntryResponse])
async def find_all(db: Session = Depends(database_conector.get_database_session)):
    financial_expense_entries = financial_expense_entry_repository.find_all(db)
    return [FinancialExpenseEntryResponse.from_orm(financial_expense_entry) for financial_expense_entry in financial_expense_entries]


@financial_expense_entries_router.delete(path="/{financial_expense_entry_id}")
def delete(financial_expense_entry_id: int, db: Session = Depends(database_conector.get_database_session)):
    financial_expense_entry_repository.delete_by_id(db, financial_expense_entry_id)
