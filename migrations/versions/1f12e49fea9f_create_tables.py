"""Create tables

Revision ID: 1f12e49fea9f
Revises: 
Create Date: 2024-04-11 13:23:25.154035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f12e49fea9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bursary',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('fund_amount', sa.Float(), nullable=False),
    sa.Column('contact_person', sa.String(length=100), nullable=False),
    sa.Column('photo_url', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('id_no', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('beneficiary',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('bursary_id', sa.String(length=36), nullable=False),
    sa.Column('amount_allocated', sa.Float(), nullable=False),
    sa.Column('date_allocated', sa.Date(), nullable=False),
    sa.Column('disbursed', sa.Boolean(), nullable=False),
    sa.Column('date_disbursed', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['bursary_id'], ['bursary.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('declaration_documents',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('individual_declaration', sa.String(length=500), nullable=False),
    sa.Column('parent_declaration', sa.String(length=500), nullable=False),
    sa.Column('religious_leader_declaration', sa.String(length=500), nullable=False),
    sa.Column('local_authority_declaration', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('education_details',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('institution_type', mysql.ENUM('primary', 'secondary', 'tetiary'), nullable=False),
    sa.Column('institution_name', sa.String(length=100), nullable=False),
    sa.Column('institution_code', sa.String(length=100), nullable=True),
    sa.Column('level', sa.String(length=100), nullable=False),
    sa.Column('campus', sa.String(length=100), nullable=True),
    sa.Column('course', sa.String(length=100), nullable=False),
    sa.Column('mode_of_study', sa.String(length=100), nullable=False),
    sa.Column('funding_source', sa.String(length=100), nullable=False),
    sa.Column('details', sa.String(length=500), nullable=True),
    sa.Column('grade', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('parent_guardian',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('parent_type', mysql.ENUM('mother', 'father', 'guardian'), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('occupation', sa.String(length=100), nullable=False),
    sa.Column('main_income_source', sa.String(length=100), nullable=False),
    sa.Column('other_income_source', sa.String(length=100), nullable=True),
    sa.Column('employment_status', mysql.ENUM('yes', 'no', 'retired', 'self_employed'), nullable=False),
    sa.Column('average_monthly_income', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('siblings',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('relationship', sa.String(length=100), nullable=False),
    sa.Column('institution', sa.String(length=100), nullable=False),
    sa.Column('level', sa.String(length=100), nullable=False),
    sa.Column('total_annual_fees', sa.Float(), nullable=False),
    sa.Column('paid', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('studentdetails',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('contact_phone_number', sa.String(length=20), nullable=False),
    sa.Column('photo_url', sa.String(length=500), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('place_of_birth', sa.String(length=100), nullable=False),
    sa.Column('village', sa.String(length=100), nullable=False),
    sa.Column('ward', sa.String(length=100), nullable=False),
    sa.Column('constituency', sa.String(length=100), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('needy_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('studentdetails')
    op.drop_table('siblings')
    op.drop_table('parent_guardian')
    op.drop_table('education_details')
    op.drop_table('declaration_documents')
    op.drop_table('beneficiary')
    op.drop_table('users')
    op.drop_table('bursary')
    # ### end Alembic commands ###
