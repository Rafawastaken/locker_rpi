"""empty message

Revision ID: 162651cf40c0
Revises: 8b19878e640e
Create Date: 2022-09-09 01:27:23.409288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162651cf40c0'
down_revision = '8b19878e640e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'apelido')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('apelido', sa.VARCHAR(length=50), nullable=False))
    # ### end Alembic commands ###
