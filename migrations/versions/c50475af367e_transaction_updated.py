"""transaction updated

Revision ID: c50475af367e
Revises: 4a905f7fb497
Create Date: 2023-08-07 12:26:24.033069

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c50475af367e"
down_revision = "4a905f7fb497"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("transaction", sa.Column("portfolio_id", sa.UUID(), nullable=False))
    op.drop_constraint(
        "transaction_portfolio_stock_id_fkey", "transaction", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "transaction", "portfolio", ["portfolio_id"], ["portfolio_id"]
    )
    op.drop_column("transaction", "portfolio_stock_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "transaction",
        sa.Column("portfolio_stock_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "transaction", type_="foreignkey")
    op.create_foreign_key(
        "transaction_portfolio_stock_id_fkey",
        "transaction",
        "portfolio_stock",
        ["portfolio_stock_id"],
        ["portfolio_stock_id"],
    )
    op.drop_column("transaction", "portfolio_id")
    # ### end Alembic commands ###
