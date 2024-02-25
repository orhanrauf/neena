"""Adjust TaskDefinition for input fields 2

Revision ID: dd69139d321a
Revises: 7f9e3611ddb9
Create Date: 2024-02-23 22:33:19.290947

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = 'dd69139d321a'
down_revision = '7f9e3611ddb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_definition', sa.Column('input_type', sa.String(), nullable=False))
    op.add_column('task_definition', sa.Column('input_yml', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_definition', 'input_yml')
    op.drop_column('task_definition', 'input_type')
    # ### end Alembic commands ###
