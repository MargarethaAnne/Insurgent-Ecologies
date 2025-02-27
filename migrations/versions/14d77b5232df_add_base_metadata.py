"""add base metadata

Revision ID: 14d77b5232df
Revises: b4351611c5aa
Create Date: 2021-03-31 11:36:06.460696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d77b5232df'
down_revision = 'b4351611c5aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('crops_id')

    with op.batch_alter_table('crops', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('company_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('crops', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'companies', ['company_id'], ['id'])

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('crops_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'crops', ['crops_id'], ['id'])

    # ### end Alembic commands ###
