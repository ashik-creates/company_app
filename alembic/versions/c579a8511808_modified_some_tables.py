"""modified some tables

Revision ID: c579a8511808
Revises: 69b996377d83
Create Date: 2024-09-02 20:28:12.434721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c579a8511808'
down_revision: Union[str, None] = '69b996377d83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('super_admins', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('super_admins', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('super_admins', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('super_admins', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('super_admins', 'created_at')
    op.drop_column('super_admins', 'hashed_password')
    # ### end Alembic commands ###
