"""Create flights and bookings tables

Revision ID: 79f49a940bde
Revises: c47ecbf163d4
Create Date: 2024-02-05 20:06:47.037971

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT

# revision identifiers, used by Alembic.
revision = '79f49a940bde'
down_revision = 'c47ecbf163d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_number', sa.String(), nullable=False),
    sa.Column('departure_airport', sa.String(), nullable=False),
    sa.Column('destination_airport', sa.String(), nullable=False),
    sa.Column('departure_datetime', sa.DateTime(), nullable=False),
    sa.Column('available_seats', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight_number')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('seat_number', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('admins', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('bookings')
    op.drop_table('flights')
    # ### end Alembic commands ###