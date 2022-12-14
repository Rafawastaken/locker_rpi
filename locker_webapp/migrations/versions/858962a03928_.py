"""empty message

Revision ID: 858962a03928
Revises: 87d96f151436
Create Date: 2022-09-15 21:34:10.893503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '858962a03928'
down_revision = '87d96f151436'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raspberry', sa.Column('key', sa.String(length=50), nullable=False))
    op.drop_column('raspberry', 'seed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raspberry', sa.Column('seed', sa.VARCHAR(length=50), nullable=False))
    op.drop_column('raspberry', 'key')
    # ### end Alembic commands ###
