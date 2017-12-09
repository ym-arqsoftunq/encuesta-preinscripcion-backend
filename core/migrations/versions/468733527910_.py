"""empty message

Revision ID: 468733527910
Revises: 55d856a853d6
Create Date: 2017-12-09 11:14:22.863982

"""

# revision identifiers, used by Alembic.
revision = '468733527910'
down_revision = '55d856a853d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('materiaresponses')
    op.add_column('materias', sa.Column('oferta_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'materias', 'ofertas', ['oferta_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'materias', type_='foreignkey')
    op.drop_column('materias', 'oferta_id')
    op.create_table('materiaresponses',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('materia_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('descripcion', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['materia_id'], ['materias.id'], name='materiaresponses_materia_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='materiaresponses_pkey')
    )
    # ### end Alembic commands ###
