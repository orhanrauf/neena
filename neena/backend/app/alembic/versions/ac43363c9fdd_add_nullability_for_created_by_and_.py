"""Add nullability for created_by and modified_by for Task Definition

Revision ID: ac43363c9fdd
Revises: 32cad5473878
Create Date: 2023-07-31 15:42:34.910616

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = 'ac43363c9fdd'
down_revision = '32cad5473878'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task_definition', 'created_by_email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('task_definition', 'modified_by_email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task_definition', 'modified_by_email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('task_definition', 'created_by_email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
