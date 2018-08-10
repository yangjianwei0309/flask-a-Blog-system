"""empty message

Revision ID: 22f7bd39a2bb
Revises: ee651b4c4469
Create Date: 2018-08-08 17:19:51.652829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f7bd39a2bb'
down_revision = 'ee651b4c4469'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('content', sa.String(length=1000), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'content')
    # ### end Alembic commands ###
