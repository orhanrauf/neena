"""Change nullability of flow_request instruction

Revision ID: 32cad5473878
Revises: 4575de758b88
Create Date: 2023-07-29 14:17:06.946264

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = '32cad5473878'
down_revision = '4575de758b88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
