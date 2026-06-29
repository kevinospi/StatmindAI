"""agregar_titulo_a_informes

Revision ID: a4cfd29be7f5
Revises: 9ffaeed3a04a
Create Date: 2026-06-29 07:13:50.893911+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a4cfd29be7f5'
down_revision: Union[str, None] = '9ffaeed3a04a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "informes",
        sa.Column("titulo", sa.String(length=150), nullable=False, server_default="Informe sin título"),
    )


def downgrade() -> None:
    op.drop_column("informes", "titulo")