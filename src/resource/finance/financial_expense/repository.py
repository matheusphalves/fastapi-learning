from sqlalchemy.orm import Session

from src.database.models import FinancialExpense, FinancialUser
from src.util.base_repository import BaseRepository


class FinancialExpenseRepository(BaseRepository):

    def __init__(self):
        self.entityModel = FinancialExpense

    def save(self, db: Session, financial_expense: FinancialExpense) -> any:

        if self.related_fk_exists(db, FinancialUser, financial_expense.financial_user_id):
            return super().save(db, financial_expense)
        return None

    def update(self, db: Session, financial_expense: FinancialExpense) -> any:

        if self.related_relationship_exists(db, FinancialUser, financial_expense.id, financial_expense.financial_user_id):
            return super().update(db, financial_expense)
        return None
