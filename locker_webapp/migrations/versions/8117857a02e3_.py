"""empty message

Revision ID: 8117857a02e3
Revises: 858962a03928
Create Date: 2022-09-17 18:43:10.950986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8117857a02e3'
down_revision = '858962a03928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('raspberry')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raspberry',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=50), nullable=False),
    sa.Column('key', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    # ### end Alembic commands ###
