"""added new super admin table

Revision ID: 49afabf001db
Revises: 47c3bcd2207e
Create Date: 2024-09-02 20:03:31.510950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49afabf001db'
down_revision: Union[str, None] = '47c3bcd2207e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('super_admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('companies', sa.Column('email', sa.String(), nullable=False))
    op.add_column('companies', sa.Column('password', sa.String(), nullable=False))
    op.add_column('companies', sa.Column('is_super_admin', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'companies', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_column('companies', 'is_super_admin')
    op.drop_column('companies', 'password')
    op.drop_column('companies', 'email')
    op.drop_table('super_admins')
    # ### end Alembic commands ###
