"""empty message

Revision ID: 6750c0d9a1d2
Revises: d59bb3f57c52
Create Date: 2017-12-08 14:28:01.229303

"""

# revision identifiers, used by Alembic.
revision = '6750c0d9a1d2'
down_revision = 'd59bb3f57c52'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('name', sa.String(length=50), nullable=True))
    op.drop_constraint('roles_nombre_key', 'roles', type_='unique')
    op.create_unique_constraint(None, 'roles', ['name'])
    op.drop_column('roles', 'nombre')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('nombre', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'roles', type_='unique')
    op.create_unique_constraint('roles_nombre_key', 'roles', ['nombre'])
    op.drop_column('roles', 'name')
    # ### end Alembic commands ###
