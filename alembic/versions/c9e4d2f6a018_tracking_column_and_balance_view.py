"""tracking column and balance view

Revision ID: c9e4d2f6a018
Revises: b3d7e9a1f042
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c9e4d2f6a018'
down_revision: Union[str, None] = 'b3d7e9a1f042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
        CREATE OR REPLACE VIEW bank_account_balance_view AS
        SELECT
            ba.account_id,
            ba.account_name,
            ba.account_type,
            COALESCE(ba.start_value, 0)                                                              AS start_value,
            COALESCE(SUM(t.value) FILTER (WHERE t.tracking = true AND t.value > 0), 0)              AS total_gains,
            COALESCE(SUM(ABS(t.value)) FILTER (WHERE t.tracking = true AND t.value < 0), 0)         AS total_expenses,
            COALESCE(ba.start_value, 0)
                + COALESCE(SUM(t.value) FILTER (WHERE t.tracking = true AND t.value > 0), 0)
                - COALESCE(SUM(ABS(t.value)) FILTER (WHERE t.tracking = true AND t.value < 0), 0)   AS current_balance
        FROM bank_accounts ba
        LEFT JOIN transactions t ON t.account_id = ba.account_id
        GROUP BY ba.account_id, ba.account_name, ba.account_type, ba.start_value
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS bank_account_balance_view")
    op.drop_column('transactions', 'tracking')
