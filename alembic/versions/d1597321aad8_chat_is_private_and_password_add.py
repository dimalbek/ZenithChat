"""chat is_private and password add

Revision ID: d1597321aad8
Revises: 39c98042640e
Create Date: 2024-05-03 00:11:00.774820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1597321aad8'
down_revision: Union[str, None] = '39c98042640e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_private', sa.Boolean(), nullable=False, server_default=sa.text('false')))
        batch_op.add_column(sa.Column('password_hashed', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_column('is_private')
        batch_op.drop_column('password_hashed')
