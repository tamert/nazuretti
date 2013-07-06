"""add order fields to product

Revision ID: 48369f836dd8
Revises: None
Create Date: 2013-07-06 15:19:32.910091

"""

# revision identifiers, used by Alembic.
revision = '48369f836dd8'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('products', sa.Column('is_orderable', sa.Boolean))

def downgrade():
  op.drop_column('products', 'is_orderable')
