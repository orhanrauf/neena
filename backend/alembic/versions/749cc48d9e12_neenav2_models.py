"""NeenaV2 models

Revision ID: 749cc48d9e12
Revises: 4d129cc23ac3
Create Date: 2024-01-28 14:58:32.270415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import app.models.types

# revision identifiers, used by Alembic.
revision = '749cc48d9e12'
down_revision = '4d129cc23ac3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('integration',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('short_name', sa.String(), nullable=False),
    sa.Column('uses_api_key', sa.Boolean(), nullable=False),
    sa.Column('uses_sso_key', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integration_id'), 'integration', ['id'], unique=False)
    op.create_table('organization',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('auth0_id', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organization_auth0_id'), 'organization', ['auth0_id'], unique=True)
    op.create_index(op.f('ix_organization_id'), 'organization', ['id'], unique=False)
    op.create_table('integration_credential',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('intergation', sa.UUID(), nullable=False),
    sa.Column('created_by_email', sa.String(), nullable=False),
    sa.Column('modified_by_email', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('credential', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['intergation'], ['integration.id'], ),
    sa.ForeignKeyConstraint(['modified_by_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integration_credential_id'), 'integration_credential', ['id'], unique=False)
    op.create_table('dependency',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('flow', sa.UUID(), nullable=False),
    sa.Column('source_task_operation', sa.UUID(), nullable=False),
    sa.Column('target_task_operation', sa.UUID(), nullable=False),
    sa.Column('instruction', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['flow'], ['flow.id'], ),
    sa.ForeignKeyConstraint(['source_task_operation'], ['task_operation.id'], ),
    sa.ForeignKeyConstraint(['target_task_operation'], ['task_operation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dependency_id'), 'dependency', ['id'], unique=False)
    op.create_table('task_prep_prompt',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('task_run', sa.UUID(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['task_run'], ['task_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_prep_prompt_id'), 'task_prep_prompt', ['id'], unique=False)
    op.create_table('task_prep_answer',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('natural_language_explanation', sa.String(), nullable=False),
    sa.Column('task_prep_prompt', sa.UUID(), nullable=False),
    sa.Column('task_run', sa.UUID(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('has_python_execution', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['task_prep_prompt'], ['task_prep_prompt.id'], ),
    sa.ForeignKeyConstraint(['task_run'], ['task_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_prep_answer_id'), 'task_prep_answer', ['id'], unique=False)
    op.drop_index('ix_task_log_id', table_name='task_log')
    op.drop_index('ix_task_log_task_run_id', table_name='task_log')
    op.drop_index('ix_task_log_timestamp_utc', table_name='task_log')
    op.drop_table('task_log')
    op.drop_index('ix_token_token', table_name='token')
    op.drop_table('token')
    op.add_column('flow', sa.Column('organization', sa.UUID(), nullable=True))
    op.drop_constraint('flow_flow_request_fkey', 'flow', type_='foreignkey')
    op.create_foreign_key(None, 'flow', 'organization', ['organization'], ['id'])
    op.drop_column('flow', 'flow_request')
    op.add_column('flow_request', sa.Column('flow', sa.UUID(), nullable=True))
    op.add_column('flow_request', sa.Column('organization', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'flow_request', 'flow', ['flow'], ['id'])
    op.create_foreign_key(None, 'flow_request', 'organization', ['organization'], ['id'])
    op.add_column('flow_run', sa.Column('organization', sa.UUID(), nullable=True))
    op.add_column('flow_run', sa.Column('flow', sa.UUID(), nullable=False))
    op.add_column('flow_run', sa.Column('triggered_time', sa.DateTime(timezone=True), nullable=True))
    op.add_column('flow_run', sa.Column('triggered_by', sa.String(), nullable=True))
    op.drop_constraint('flow_run_flow_id_fkey', 'flow_run', type_='foreignkey')
    op.create_foreign_key(None, 'flow_run', 'organization', ['organization'], ['id'])
    op.create_foreign_key(None, 'flow_run', 'flow', ['flow'], ['id'])
    op.create_foreign_key(None, 'flow_run', 'user', ['triggered_by'], ['email'])
    op.drop_column('flow_run', 'flow_id')
    op.add_column('task_definition', sa.Column('python_method_name', sa.String(), nullable=False))
    op.add_column('task_operation', sa.Column('instruction', sa.String(), nullable=True))
    op.add_column('task_operation', sa.Column('organization', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'task_operation', 'organization', ['organization'], ['id'])
    op.drop_column('task_operation', 'explanation')
    op.drop_column('task_operation', 'z')
    op.drop_column('task_operation', 'arguments')
    op.add_column('task_run', sa.Column('task_operation', sa.UUID(), nullable=False))
    op.add_column('task_run', sa.Column('flow_run', sa.UUID(), nullable=True))
    op.add_column('task_run', sa.Column('result', sa.JSON(), nullable=True))
    op.drop_constraint('task_run_task_operation_id_fkey', 'task_run', type_='foreignkey')
    op.drop_constraint('task_run_flow_run_id_fkey', 'task_run', type_='foreignkey')
    op.create_foreign_key(None, 'task_run', 'flow_run', ['flow_run'], ['id'])
    op.create_foreign_key(None, 'task_run', 'task_operation', ['task_operation'], ['id'])
    op.drop_column('task_run', 'status')
    op.drop_column('task_run', 'flow_run_id')
    op.drop_column('task_run', 'task_operation_id')
    op.add_column('user', sa.Column('organization', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'user', 'organization', ['organization'], ['id'])
    op.drop_column('user', 'modified_date')
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('modified_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'organization')
    op.add_column('task_run', sa.Column('task_operation_id', sa.UUID(), autoincrement=False, nullable=False))
    op.add_column('task_run', sa.Column('flow_run_id', sa.UUID(), autoincrement=False, nullable=False))
    op.add_column('task_run', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'task_run', type_='foreignkey')
    op.drop_constraint(None, 'task_run', type_='foreignkey')
    op.create_foreign_key('task_run_flow_run_id_fkey', 'task_run', 'flow_run', ['flow_run_id'], ['id'])
    op.create_foreign_key('task_run_task_operation_id_fkey', 'task_run', 'task_operation', ['task_operation_id'], ['id'])
    op.drop_column('task_run', 'result')
    op.drop_column('task_run', 'flow_run')
    op.drop_column('task_run', 'task_operation')
    op.add_column('task_operation', sa.Column('arguments', sa.TEXT(), autoincrement=False, nullable=False))
    op.add_column('task_operation', sa.Column('z', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('task_operation', sa.Column('explanation', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task_operation', type_='foreignkey')
    op.drop_column('task_operation', 'organization')
    op.drop_column('task_operation', 'instruction')
    op.drop_column('task_definition', 'python_method_name')
    op.add_column('flow_run', sa.Column('flow_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'flow_run', type_='foreignkey')
    op.drop_constraint(None, 'flow_run', type_='foreignkey')
    op.drop_constraint(None, 'flow_run', type_='foreignkey')
    op.create_foreign_key('flow_run_flow_id_fkey', 'flow_run', 'flow', ['flow_id'], ['id'])
    op.drop_column('flow_run', 'triggered_by')
    op.drop_column('flow_run', 'triggered_time')
    op.drop_column('flow_run', 'flow')
    op.drop_column('flow_run', 'organization')
    op.drop_constraint(None, 'flow_request', type_='foreignkey')
    op.drop_constraint(None, 'flow_request', type_='foreignkey')
    op.drop_column('flow_request', 'organization')
    op.drop_column('flow_request', 'flow')
    op.add_column('flow', sa.Column('flow_request', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'flow', type_='foreignkey')
    op.create_foreign_key('flow_flow_request_fkey', 'flow', 'flow_request', ['flow_request'], ['id'])
    op.drop_column('flow', 'organization')
    op.create_table('token',
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_valid', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('authenticates_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['authenticates_id'], ['user.id'], name='token_authenticates_id_fkey'),
    sa.PrimaryKeyConstraint('token', name='token_pkey')
    )
    op.create_index('ix_token_token', 'token', ['token'], unique=False)
    op.create_table('task_log',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('timestamp_utc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('task_run_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('flow_run_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['flow_run_id'], ['flow_run.id'], name='task_log_flow_run_id_fkey'),
    sa.ForeignKeyConstraint(['task_run_id'], ['task_run.id'], name='task_log_task_run_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='task_log_pkey')
    )
    op.create_index('ix_task_log_timestamp_utc', 'task_log', ['timestamp_utc'], unique=False)
    op.create_index('ix_task_log_task_run_id', 'task_log', ['task_run_id'], unique=False)
    op.create_index('ix_task_log_id', 'task_log', ['id'], unique=False)
    op.drop_index(op.f('ix_task_prep_answer_id'), table_name='task_prep_answer')
    op.drop_table('task_prep_answer')
    op.drop_index(op.f('ix_task_prep_prompt_id'), table_name='task_prep_prompt')
    op.drop_table('task_prep_prompt')
    op.drop_index(op.f('ix_dependency_id'), table_name='dependency')
    op.drop_table('dependency')
    op.drop_index(op.f('ix_integration_credential_id'), table_name='integration_credential')
    op.drop_table('integration_credential')
    op.drop_index(op.f('ix_organization_id'), table_name='organization')
    op.drop_index(op.f('ix_organization_auth0_id'), table_name='organization')
    op.drop_table('organization')
    op.drop_index(op.f('ix_integration_id'), table_name='integration')
    op.drop_table('integration')
    # ### end Alembic commands ###
