"""fresh db

Revision ID: 338039df795c
Revises: 
Create Date: 2019-03-13 13:45:42.682760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '338039df795c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomNum', sa.String(length=64), nullable=True),
    sa.Column('ac', sa.Boolean(), nullable=True),
    sa.Column('projector', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('fullname', sa.String(length=64), nullable=True),
    sa.Column('position', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purpose', sa.String(length=64), nullable=True),
    sa.Column('roomID', sa.Integer(), nullable=True),
    sa.Column('bookerID', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('startTime', sa.DateTime(), nullable=True),
    sa.Column('endTime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bookerID'], ['user.id'], ),
    sa.ForeignKeyConstraint(['roomID'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('purpose')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('room')
    # ### end Alembic commands ###
