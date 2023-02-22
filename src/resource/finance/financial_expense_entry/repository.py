from sqlalchemy.orm import Session

from src.database.models import FinancialExpenseEntry, FinancialExpense
from src.util.base_repository import BaseRepository


class FinancialExpenseEntryRepository(BaseRepository):
    def __init__(self):
        self.entityModel = FinancialExpenseEntry

    def save(self, db: Session, financial_expense_entry: FinancialExpenseEntry) -> any:

        if self.related_fk_exists(db, FinancialExpense, financial_expense_entry.financial_expense_id):
            return super().save(db, financial_expense_entry)
        return None

    def update_by_custom_column_value(self, db: Session, financial_expense_entry: FinancialExpenseEntry) -> any:

        if self.related_relationship_exists(db, FinancialExpense, financial_expense_entry.id,
                                            financial_expense_entry.financial_expense_id) is not None:
            return super().update(db, financial_expense_entry)

        return None