"""drop posts and votes

Revision ID: cbde86227312
Revises: 79f49a940bde
Create Date: 2024-02-06 11:58:37.783247

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cbde86227312'
down_revision = '79f49a940bde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade():
    pass