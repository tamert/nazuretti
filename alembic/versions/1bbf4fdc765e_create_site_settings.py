"""create site_settings

Revision ID: 1bbf4fdc765e
Revises: 700d100bbdc
Create Date: 2013-07-29 22:28:36.098010

"""

# revision identifiers, used by Alembic.
revision = '1bbf4fdc765e'
down_revision = '700d100bbdc'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
  op.create_table('site_settings',
    sa.Column('id', sa.INTEGER, primary_key=True),
    sa.Column('facebook', sa.VARCHAR(250)),
    sa.Column('twitter',  sa.VARCHAR(250)),
    sa.Column('order_phone', sa.VARCHAR(250)),
    sa.Column('order_email', sa.VARCHAR(250)),
    sa.Column('contact_phone', sa.VARCHAR(250)),
    sa.Column('contact_email', sa.VARCHAR(250))
    )

  site_settings = table('site_settings')
  op.bulk_insert(site_settings, [
    dict(id=1, facebook='', twitter='', order_phone='', order_email='', contact_phone='', contact_email='')
    ])


def downgrade():
  op.drop_table('site_settings')
