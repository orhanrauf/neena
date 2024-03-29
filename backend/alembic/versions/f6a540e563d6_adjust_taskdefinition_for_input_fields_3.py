"""Adjust TaskDefinition for input fields 3

Revision ID: f6a540e563d6
Revises: dd69139d321a
Create Date: 2024-02-23 22:35:47.540790

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = 'f6a540e563d6'
down_revision = 'dd69139d321a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_definition', sa.Column('parameters', app.models.task_definition.TaskParameterType(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_definition', 'parameters')
    # ### end Alembic commands ###
