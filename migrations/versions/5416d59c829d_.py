"""empty message

Revision ID: 5416d59c829d
Revises: 142957a40c0b
Create Date: 2022-09-15 01:14:33.342045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5416d59c829d'
down_revision = '142957a40c0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('apelido', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'apelido')
    # ### end Alembic commands ###
