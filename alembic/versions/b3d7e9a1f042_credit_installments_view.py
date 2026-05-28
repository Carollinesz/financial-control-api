"""credit_installments_view

Revision ID: b3d7e9a1f042
Revises: 5c82e3f7f27c
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'b3d7e9a1f042'
down_revision: Union[str, None] = '5c82e3f7f27c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE VIEW credit_installments_view AS
        SELECT
            t.transaction_id,
            t.account_id,
            t.description,
            t.category,
            t.transaction_date,
            t.value                                                      AS total_value,
            (t.details->>'installments')::int                            AS total_installments,
            gs.n                                                         AS installment_number,
            (t.details->>'first_payment')::date
                + make_interval(months => gs.n - 1)                      AS due_date,
            COALESCE((t.details->>'interest')::numeric, 0)               AS interest_rate,
            CASE
                WHEN COALESCE((t.details->>'interest')::numeric, 0) = 0 THEN
                    ROUND(t.value / (t.details->>'installments')::int, 4)
                ELSE
                    ROUND(
                        t.value
                        * ((t.details->>'interest')::numeric
                           * POWER(1 + (t.details->>'interest')::numeric,
                                   (t.details->>'installments')::int))
                        / (POWER(1 + (t.details->>'interest')::numeric,
                                 (t.details->>'installments')::int) - 1),
                        4)
            END                                                          AS installment_value
        FROM transactions t
        CROSS JOIN LATERAL generate_series(1, (t.details->>'installments')::int) AS gs(n)
        WHERE t.type = 'credit'
          AND t.details IS NOT NULL
          AND (t.details->>'installments') IS NOT NULL
          AND (t.details->>'first_payment') IS NOT NULL
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS credit_installments_view")
