"""add user id

Revision ID: 3ddb5857d9bc
Revises: fa828fcceff9
Create Date: 2024-07-15 02:38:53.984189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ddb5857d9bc'
down_revision = 'fa828fcceff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
