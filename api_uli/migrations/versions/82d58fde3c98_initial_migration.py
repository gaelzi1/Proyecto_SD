"""Initial migration

Revision ID: 82d58fde3c98
Revises: 
Create Date: 2024-12-08 13:44:18.640807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82d58fde3c98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('response', sa.String(length=100), nullable=True),
    sa.Column('commission', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
