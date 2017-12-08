"""empty message

Revision ID: d84a3886b6a1
Revises: 48a77c0010db
Create Date: 2017-12-08 13:50:51.559214

"""

# revision identifiers, used by Alembic.
revision = 'd84a3886b6a1'
down_revision = '48a77c0010db'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'is_active')
    # ### end Alembic commands ###
