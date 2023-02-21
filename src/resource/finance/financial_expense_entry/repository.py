from sqlalchemy.orm import Session

from src.database.models import FinancialExpenseEntry
from src.util.base_repository import BaseRepository


class FinancialExpenseRepository(BaseRepository):
    def __init__(self):
        self.entityModel = FinancialExpenseEntry

    def update(self, db: Session, financial_expense_entry: FinancialExpenseEntry) -> any:
        columnName = "financial_expense_id"
        matchValue = financial_expense_entry.financial_expense_id
        return super().update(db, financial_expense_entry, columnName, matchValue)