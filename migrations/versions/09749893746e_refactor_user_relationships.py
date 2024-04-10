"""Refactor User Relationships

Revision ID: 09749893746e
Revises: 9a32486feca0
Create Date: 2024-04-11 01:24:10.536133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09749893746e'
down_revision = '9a32486feca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('beneficiary', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('beneficiary_student_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['student_id'], ['id'])

    with op.batch_alter_table('bursary', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('declaration_documents', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('declaration_documents_student_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['student_id'], ['id'])

    with op.batch_alter_table('education_details', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('parent_guardian', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('parent_guardian_student_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['student_id'], ['id'])

    with op.batch_alter_table('siblings', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('siblings_student_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['student_id'], ['id'])

    with op.batch_alter_table('studentdetails', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('studentdetails', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('siblings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('siblings_student_id_fkey', 'studentdetails', ['student_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('parent_guardian', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('parent_guardian_student_id_fkey', 'studentdetails', ['student_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('education_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('declaration_documents', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('declaration_documents_student_id_fkey', 'studentdetails', ['student_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('bursary', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('beneficiary', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('beneficiary_student_id_fkey', 'studentdetails', ['student_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
