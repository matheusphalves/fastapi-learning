from sqlalchemy.orm import Session

from src.database.models import FinancialUser
from src.util.base_repository import BaseRepository


class FinancialUserRepository(BaseRepository):

    def __init__(self):
        self.entityModel = FinancialUser

    def update(self, db: Session, financial_user: FinancialUser) -> any:
        columnName = "login"
        matchValue = financial_user.login
        return super().update(db, financial_user, columnName, matchValue)