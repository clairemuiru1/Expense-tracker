"""Added Bills

Revision ID: 573387bae8a6
Revises: 43b842f9c6bb
Create Date: 2024-04-13 12:41:17.021866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '573387bae8a6'
down_revision = '43b842f9c6bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bill')
    # ### end Alembic commands ###
