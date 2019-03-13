"""room booking added

Revision ID: 771b56bb857b
Revises: 74c54334f707
Create Date: 2019-03-13 12:04:33.189799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '771b56bb857b'
down_revision = '74c54334f707'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomNum', sa.String(length=64), nullable=False),
    sa.Column('ac', sa.Boolean(), nullable=True),
    sa.Column('projector', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
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
    op.drop_index('ix_post_timestamp', table_name='post')
    op.drop_table('post')
    op.add_column('user', sa.Column('fullname', sa.String(length=64), nullable=False))
    op.add_column('user', sa.Column('position', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'position')
    op.drop_column('user', 'fullname')
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_post_timestamp', 'post', ['timestamp'], unique=False)
    op.drop_table('booking')
    op.drop_table('room')
    # ### end Alembic commands ###