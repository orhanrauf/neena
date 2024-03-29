"""Add run models

Revision ID: 97f6680166b8
Revises: fe414de8b9c7
Create Date: 2023-08-07 15:36:21.718730

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = '97f6680166b8'
down_revision = 'fe414de8b9c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flow_run',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('flow_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['flow_id'], ['flow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flow_run_id'), 'flow_run', ['id'], unique=False)
    op.create_table('task_run',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('task_operation_id', sa.UUID(), nullable=False),
    sa.Column('flow_run_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['flow_run_id'], ['flow_run.id'], ),
    sa.ForeignKeyConstraint(['task_operation_id'], ['task_operation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_run_id'), 'task_run', ['id'], unique=False)
    op.create_table('task_log',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('timestamp_utc', sa.DateTime(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('task_run_id', sa.UUID(), nullable=True),
    sa.Column('flow_run_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['flow_run_id'], ['flow_run.id'], ),
    sa.ForeignKeyConstraint(['task_run_id'], ['task_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_log_id'), 'task_log', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_log_id'), table_name='task_log')
    op.drop_table('task_log')
    op.drop_index(op.f('ix_task_run_id'), table_name='task_run')
    op.drop_table('task_run')
    op.drop_index(op.f('ix_flow_run_id'), table_name='flow_run')
    op.drop_table('flow_run')
    # ### end Alembic commands ###
