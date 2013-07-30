"""site settings bank accounts

Revision ID: 546524dd2d90
Revises: 1bbf4fdc765e
Create Date: 2013-07-30 23:45:54.810629

"""

# revision identifiers, used by Alembic.
revision = '546524dd2d90'
down_revision = '1bbf4fdc765e'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('site_settings', sa.Column('bank_person', sa.Text))
  op.add_column('site_settings', sa.Column('bank_name', sa.Text))
  op.add_column('site_settings', sa.Column('bank_iban', sa.Text))

def downgrade():
  op.drop_column('site_settings', 'bank_person')
  op.drop_column('site_settings', 'bank_name')
  op.drop_column('site_settings', 'bank_iban')
