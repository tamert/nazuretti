"""gallery add description

Revision ID: 700d100bbdc
Revises: 3734d3356964
Create Date: 2013-07-29 00:05:04.259323

"""

# revision identifiers, used by Alembic.
revision = '700d100bbdc'
down_revision = '3734d3356964'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('pictures', sa.Column('description', sa.Text))

def downgrade():
  op.drop_column('pictures', 'description')
