"""add assoc table

Revision ID: 091d401fb04a
Revises: e6bc5c127574
Create Date: 2021-03-30 20:15:56.146480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '091d401fb04a'
down_revision = 'e6bc5c127574'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('companies_crops_assoc')
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

    op.create_table('companies_crops_assoc',
    sa.Column('companies_crops_id', sa.INTEGER(), nullable=True),
    sa.Column('companies_crops', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['companies_crops'], ['crops.id'], name='fk_companies_crops_assoc_companies_crops_crops'),
    sa.ForeignKeyConstraint(['companies_crops_id'], ['companies.id'], name='fk_companies_crops_assoc_companies_crops_id_companies')
    )
    # ### end Alembic commands ###
