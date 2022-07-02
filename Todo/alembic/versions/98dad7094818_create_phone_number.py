"""create phone number

Revision ID: 98dad7094818
Revises: 
Create Date: 2022-07-03 00:21:18.535107

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '98dad7094818'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
