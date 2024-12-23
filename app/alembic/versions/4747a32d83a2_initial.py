"""initial

Revision ID: 4747a32d83a2
Revises: 
Create Date: 2024-01-08 10:25:40.156856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4747a32d83a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requestlog',
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('authorization', sa.String(length=256), nullable=True),
    sa.Column('method', sa.String(length=10), nullable=True),
    sa.Column('service_name', sa.String(length=50), nullable=True),
    sa.Column('ip', sa.String(length=50), nullable=True),
    sa.Column('request', sa.Text(), nullable=True),
    sa.Column('response', sa.Text(), nullable=True),
    sa.Column('trace', sa.Text(), nullable=True),
    sa.Column('is_deleted', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requestlog_authorization'), 'requestlog', ['authorization'], unique=False)
    op.create_index(op.f('ix_requestlog_created'), 'requestlog', ['created'], unique=False)
    op.create_index(op.f('ix_requestlog_id'), 'requestlog', ['id'], unique=False)
    op.create_index(op.f('ix_requestlog_ip'), 'requestlog', ['ip'], unique=False)
    op.create_index(op.f('ix_requestlog_is_deleted'), 'requestlog', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_requestlog_method'), 'requestlog', ['method'], unique=False)
    op.create_index(op.f('ix_requestlog_modified'), 'requestlog', ['modified'], unique=False)
    op.create_index(op.f('ix_requestlog_request'), 'requestlog', ['request'], unique=False)
    op.create_index(op.f('ix_requestlog_service_name'), 'requestlog', ['service_name'], unique=False)
    op.create_index(op.f('ix_requestlog_trace'), 'requestlog', ['trace'], unique=False)
    op.create_table('user',
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_created'), 'user', ['created'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_is_deleted'), 'user', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_user_modified'), 'user', ['modified'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_modified'), table_name='user')
    op.drop_index(op.f('ix_user_is_deleted'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_created'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_requestlog_trace'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_service_name'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_request'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_modified'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_method'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_is_deleted'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_ip'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_id'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_created'), table_name='requestlog')
    op.drop_index(op.f('ix_requestlog_authorization'), table_name='requestlog')
    op.drop_table('requestlog')
    # ### end Alembic commands ###
