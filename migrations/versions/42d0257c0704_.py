"""empty message

Revision ID: 42d0257c0704
Revises: None
Create Date: 2016-02-20 01:20:46.219637

"""

# revision identifiers, used by Alembic.
revision = '42d0257c0704'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_lock')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_lock',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('state', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
