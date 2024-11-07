"""update_tables

Revision ID: 8b5eb353fc3d
Revises: 80d67dfeca8b
Create Date: 2024-11-07 00:08:52.194944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b5eb353fc3d'
down_revision: Union[str, None] = '80d67dfeca8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
