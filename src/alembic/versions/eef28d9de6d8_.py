"""empty message

Revision ID: eef28d9de6d8
Revises: 993e6195f17b
Create Date: 2024-09-08 23:12:12.707784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eef28d9de6d8'
down_revision = '993e6195f17b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_models',
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('filesize', sa.Integer(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.Column('etag', sa.String(), nullable=False),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_models')
    # ### end Alembic commands ###