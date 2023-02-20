from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from src.database.database import Base


class FinancialUser(Base):
    __tablename__ = "financial_user"

    id: int = Column(Integer, primary_key=True, index=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    login: str = Column(String(255), nullable=False)
    password: str = Column(String(100), nullable=False)
    create_date: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    update_date: DateTime = Column(DateTime(timezone=True), onupdate=func.now())
