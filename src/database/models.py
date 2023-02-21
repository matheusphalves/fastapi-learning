from typing import List

from sqlalchemy import Column, DateTime, String, ForeignKey, Double
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func

from src.database.database import Base, database_conector


class FinancialUser(Base):
    __tablename__ = "financial_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    login: str = Column(String(255), nullable=False)
    password: str = Column(String(100), nullable=False)
    create_date: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    update_date: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    financial_expense: Mapped[List["FinancialExpense"]] = relationship(back_populates="parent")


class FinancialExpense(Base):
    __tablename__ = "financial_expense"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    financial_user_id: Mapped[int] = mapped_column(ForeignKey("financial_user.id"))
    parent: Mapped["FinancialUser"] = relationship(back_populates="financial_expense")

    type = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    create_date: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    update_date: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    financial_expense: Mapped[List["FinancialExpenseEntry"]] = relationship(back_populates="parent")


class FinancialExpenseEntry(Base):
    __tablename__ = "financial_expense_entry"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    amount: Double = Column(Double, nullable=False)
    description = Column(String(255), nullable=False)

    create_date: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    update_date: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    financial_expense_id: Mapped[int] = mapped_column(ForeignKey("financial_expense.id"))
    parent: Mapped["FinancialExpense"] = relationship(back_populates="financial_expense")


engine = database_conector.create_engine()
