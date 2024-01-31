"""initial migration

Revision ID: 43b842f9c6bb
Revises: 
Create Date: 2024-01-31 22:52:11.148370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43b842f9c6bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('_password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('User_id', sa.Integer(), nullable=True),
    sa.Column('Category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('User_id', sa.Integer(), nullable=True),
    sa.Column('Category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('budget')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
