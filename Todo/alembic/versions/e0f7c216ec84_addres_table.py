"""addres table

Revision ID: e0f7c216ec84
Revises: 98dad7094818
Create Date: 2022-07-03 00:34:06.631182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f7c216ec84'
down_revision = '98dad7094818'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer, primary_key=True,nullable = False),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=True),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False),
    )
                    


def downgrade() -> None:
    op.drop_table('address')
