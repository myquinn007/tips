"""empty message

Revision ID: 2dcb47370d14
Revises: 3c04ca06c956
Create Date: 2024-09-04 08:28:17.878516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dcb47370d14'
down_revision = '3c04ca06c956'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment_received', schema=None) as batch_op:
        batch_op.add_column(sa.Column('download_number', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment_received', schema=None) as batch_op:
        batch_op.drop_column('download_number')

    # ### end Alembic commands ###
