"""user info

Revision ID: d3a73efdf62d
Revises: c529ba976dd5
Create Date: 2019-08-08 11:16:59.230594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3a73efdf62d'
down_revision = 'c529ba976dd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nickname', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nickname')
    # ### end Alembic commands ###