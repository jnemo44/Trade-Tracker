"""Initial migration

Revision ID: 73b7bf3dc609
Revises: 
Create Date: 2020-06-04 14:58:27.091886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73b7bf3dc609'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('open_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('open_date', sa.DateTime(), nullable=False),
    sa.Column('buy_sell', sa.String(length=5), nullable=False),
    sa.Column('ticker', sa.String(length=10), nullable=True),
    sa.Column('number_contracts', sa.Integer(), nullable=False),
    sa.Column('open_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('adjustment', sa.Boolean(), nullable=False),
    sa.Column('trade_type', sa.String(length=100), nullable=True),
    sa.Column('open_description', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('close_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('open_id', sa.Integer(), nullable=False),
    sa.Column('close_date', sa.DateTime(), nullable=False),
    sa.Column('buy_sell', sa.String(length=5), nullable=False),
    sa.Column('number_contracts', sa.Integer(), nullable=False),
    sa.Column('close_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('adjustment', sa.Boolean(), nullable=False),
    sa.Column('close_description', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['open_id'], ['open_orders.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('close_orders')
    op.drop_table('open_orders')
    # ### end Alembic commands ###
