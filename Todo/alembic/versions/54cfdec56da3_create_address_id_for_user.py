"""create address_id for user

Revision ID: 54cfdec56da3
Revises: e0f7c216ec84
Create Date: 2022-07-03 00:39:37.800216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54cfdec56da3'
down_revision = 'e0f7c216ec84'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_address', 'users', 'address', ['address_id'], ['id'],ondelete='CASCADE')


def downgrade() -> None:
    pass
    # op.drop_constraint('fk_users_address', 'users')
    # op.drop_column('users', 'address_id')
