"""Fix typo in integration for IntegrationCredential

Revision ID: 7a7571858d19
Revises: f6a540e563d6
Create Date: 2024-02-26 17:36:08.222319

"""
from alembic import op
import sqlalchemy as sa

import app.models.types

# revision identifiers, used by Alembic.
revision = '7a7571858d19'
down_revision = 'f6a540e563d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('integration_credential', sa.Column('integration', sa.UUID(), nullable=False))
    op.drop_constraint('uix_integration_created_by', 'integration_credential', type_='unique')
    op.create_unique_constraint('uix_integration_created_by', 'integration_credential', ['integration', 'created_by_email'])
    op.drop_constraint('uix_integration_modified_by', 'integration_credential', type_='unique')
    op.create_unique_constraint('uix_integration_modified_by', 'integration_credential', ['integration', 'modified_by_email'])
    op.drop_constraint('integration_credential_intergation_fkey', 'integration_credential', type_='foreignkey')
    op.create_foreign_key(None, 'integration_credential', 'integration', ['integration'], ['id'])
    op.drop_column('integration_credential', 'intergation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('integration_credential', sa.Column('intergation', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'integration_credential', type_='foreignkey')
    op.create_foreign_key('integration_credential_intergation_fkey', 'integration_credential', 'integration', ['intergation'], ['id'])
    op.drop_constraint('uix_integration_modified_by', 'integration_credential', type_='unique')
    op.create_unique_constraint('uix_integration_modified_by', 'integration_credential', ['intergation', 'modified_by_email'])
    op.drop_constraint('uix_integration_created_by', 'integration_credential', type_='unique')
    op.create_unique_constraint('uix_integration_created_by', 'integration_credential', ['intergation', 'created_by_email'])
    op.drop_column('integration_credential', 'integration')
    # ### end Alembic commands ###
