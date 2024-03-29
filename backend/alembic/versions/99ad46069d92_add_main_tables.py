"""Add main tables

Revision ID: 99ad46069d92
Revises: 8188d671489a
Create Date: 2023-07-10 20:09:43.289324

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import app.models.types

# revision identifiers, used by Alembic.
revision = '99ad46069d92'
down_revision = '8188d671489a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flow_request',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('request_metadata', app.models.types.text_pickle.TextPickleType(), nullable=True),
    sa.Column('request_instructions', sa.String(), nullable=False),
    sa.Column('request_body', sa.String(), nullable=False),
    sa.Column('created_by_email', sa.String(), nullable=False),
    sa.Column('modified_by_email', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['modified_by_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flow_request_id'), 'flow_request', ['id'], unique=False)
    op.create_table('task_definition',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('task_name', sa.String(), nullable=False),
    sa.Column('parameters', app.models.types.text_pickle.TextPickleType(), nullable=True),
    sa.Column('output_type', sa.String(), nullable=False),
    sa.Column('output_name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('python_code', sa.String(), nullable=False),
    sa.Column('created_by_email', sa.String(), nullable=False),
    sa.Column('modified_by_email', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['modified_by_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_definition_id'), 'task_definition', ['id'], unique=False)
    op.create_table('flow',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('flow_request', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by_human', sa.Boolean(), nullable=False),
    sa.Column('modified_by_human', sa.Boolean(), nullable=False),
    sa.Column('created_by_email', sa.String(), nullable=False),
    sa.Column('modified_by_email', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['flow_request'], ['flow_request.id'], ),
    sa.ForeignKeyConstraint(['modified_by_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flow_id'), 'flow', ['id'], unique=False)
    op.create_index(op.f('ix_flow_name'), 'flow', ['name'], unique=False)
    op.create_table('task_operation',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('flow', sa.UUID(), nullable=False),
    sa.Column('task_definition', sa.UUID(), nullable=False),
    sa.Column('arguments', app.models.types.text_pickle.TextPickleType(), nullable=True),
    sa.Column('explanation', sa.String(), nullable=True),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('z', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by_email', sa.String(), nullable=False),
    sa.Column('modified_by_email', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['flow'], ['flow.id'], ),
    sa.ForeignKeyConstraint(['modified_by_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['task_definition'], ['task_definition.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_operation_id'), 'task_operation', ['id'], unique=False)
    op.alter_column('token', 'is_valid',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('token', 'authenticates_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('user', 'created_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('user', 'modified_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('user', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('user', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('user', 'totp_counter')
    op.drop_column('user', 'email_validated')
    op.drop_column('user', 'totp_secret')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('totp_secret', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('email_validated', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('totp_counter', sa.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('user', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('user', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('user', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'modified_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('user', 'created_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('token', 'authenticates_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('token', 'is_valid',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_index(op.f('ix_task_operation_id'), table_name='task_operation')
    op.drop_table('task_operation')
    op.drop_index(op.f('ix_flow_name'), table_name='flow')
    op.drop_index(op.f('ix_flow_id'), table_name='flow')
    op.drop_table('flow')
    op.drop_index(op.f('ix_task_definition_id'), table_name='task_definition')
    op.drop_table('task_definition')
    op.drop_index(op.f('ix_flow_request_id'), table_name='flow_request')
    op.drop_table('flow_request')
    # ### end Alembic commands ###
