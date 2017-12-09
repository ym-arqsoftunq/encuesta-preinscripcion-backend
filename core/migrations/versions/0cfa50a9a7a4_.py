"""empty message

Revision ID: 0cfa50a9a7a4
Revises: 6750c0d9a1d2
Create Date: 2017-12-09 09:47:40.337838

"""

# revision identifiers, used by Alembic.
revision = '0cfa50a9a7a4'
down_revision = '6750c0d9a1d2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comisiones', sa.Column('cupo', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comisiones', 'cupo')
    # ### end Alembic commands ###
