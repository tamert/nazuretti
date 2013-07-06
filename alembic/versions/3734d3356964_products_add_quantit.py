"""products add quantity

Revision ID: 3734d3356964
Revises: 8b730a908d8
Create Date: 2013-07-06 20:12:08.164982

"""

# revision identifiers, used by Alembic.
revision = '3734d3356964'
down_revision = '8b730a908d8'

from alembic import op
import sqlalchemy as sa

def upgrade():
  op.add_column('products', sa.Column('quantity', sa.String))

def downgrade():
  op.drop_column('products', 'quantity')
