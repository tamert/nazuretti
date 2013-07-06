"""orderable_to_products

Revision ID: 8b730a908d8
Revises: None
Create Date: 2013-07-06 15:39:10.809407

"""

# revision identifiers, used by Alembic.
revision = '8b730a908d8'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('products', sa.Column('price', sa.String))

def downgrade():
  op.drop_column('products', 'price')
