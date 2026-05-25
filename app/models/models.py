from decimal import Decimal
from datetime import datetime, date
import json 

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, registry, MappedAsDataclass
from sqlalchemy.dialects.postgresql import JSONB

with open('./app/constants/banks.json') as f:
    avaliable_banks = json.load(f)['brazilian_banks']

avaliable_banks_sql = "(" + ", ".join(f"'{b}'" for b in avaliable_banks) + ")"


table_registry = registry()

class Base(DeclarativeBase, MappedAsDataclass):
    pass

@table_registry.mapped_as_dataclass()
class bank_account():
    __tablename__ = "bank_accounts"

    account_id:       Mapped[int]           = mapped_column(init=False, primary_key=True, autoincrement=True)
    bank_id:          Mapped[int]           = mapped_column(nullable=False)
    bank_name:        Mapped["banks"]   = relationship(
            init=False,
            primaryjoin="bank_account.bank_id == banks.bank_id",
            foreign_keys="bank_account.bank_id"
    )
    account_name:     Mapped[str]           = mapped_column(String(100), nullable=False, unique=True)  
    account_type:     Mapped[str]           = mapped_column(String(100), nullable=False)
    start_value:      Mapped[Decimal]       = mapped_column(Numeric(18, 4), nullable=True, default=0.0)
    created_at:       Mapped[datetime]      = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, init=False)

    __table_args__ = (
        CheckConstraint("-999000000000 < start_value AND start_value < 999000000000", name="check_start_value_limit"),
    )

@table_registry.mapped_as_dataclass()
class transaction:
    __tablename__ = "transactions"
    __mapper_args__ = {"polymorphic_on": "type", "polymorphic_identity": "transaction"}

    transaction_id:   Mapped[int]            = mapped_column(init=False, primary_key=True, autoincrement=True)
    account_id:       Mapped[int]            = mapped_column(nullable=False)
    transaction_date: Mapped[date]           = mapped_column(Date, nullable=False)
    value:            Mapped[Decimal]        = mapped_column(Numeric(18, 4), nullable=False)
    description:      Mapped[str]            = mapped_column(String(100), nullable=False)
    bank_account:     Mapped["bank_account"] = relationship(
            init=False,
            primaryjoin="transaction.account_id == bank_account.account_id",
            foreign_keys="transaction.account_id"
    )
    type:             Mapped[str]            = mapped_column(String(50), nullable=False, default='debit')
    details:          Mapped[dict]           = mapped_column(JSONB, nullable=True, default=None)
    category:         Mapped[str]            = mapped_column(String(100), nullable=True, default='Outros')
    created_at:       Mapped[datetime]       = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, init=False)

    def __post_init__(self):
        if self.type == "credit":
            if not self.details:
                raise ValueError("Credit transactions require the 'details' dictionary.")

            if "installments" not in self.details:
                self.details['installments'] = 1

            if "interest" not in self.details:
                self.details['interest'] = 0.0000

            installments = self.details["installments"] 
            if not (1 <= installments <= 99):
                raise ValueError("The number of installments must be between 1 and 99")
                
            if "first_payment" not in self.details:
                raise ValueError("Transações de crédito precisam de 'first_payment'.")

            fp = self.details["first_payment"]
            if isinstance(fp, str):
                try:
                    date.fromisoformat(fp)
                except ValueError:
                    raise ValueError("first_payment string must be in YYYY-MM-DD format")
            elif not isinstance(fp, date):
                raise ValueError("first_payment must be a date type or a valid ISO date string")

@table_registry.mapped_as_dataclass()
class banks():
    __tablename__ = "avaliable_banks"

    bank_id:       Mapped[int]           = mapped_column(init=False, primary_key=True, autoincrement=True)
    bank_name:     Mapped[str]           = mapped_column(String(100), nullable=False)
    created_at:    Mapped[datetime]      = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, init=False)