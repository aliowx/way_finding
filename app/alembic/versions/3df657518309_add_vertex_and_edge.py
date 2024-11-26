"""add vertex and edge

Revision ID: 3df657518309
Revises: df2350c049e9
Create Date: 2024-10-07 16:21:58.428838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df657518309'
down_revision = 'df2350c049e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vertex',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('is_deleted', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vertex_created'), 'vertex', ['created'], unique=False)
    op.create_index(op.f('ix_vertex_id'), 'vertex', ['id'], unique=False)
    op.create_index(op.f('ix_vertex_is_deleted'), 'vertex', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_vertex_modified'), 'vertex', ['modified'], unique=False)
    op.create_table('edge',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source_vertex_id', sa.Integer(), nullable=False),
    sa.Column('destination_vertex_id', sa.Integer(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('is_deleted', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['destination_vertex_id'], ['vertex.id'], ),
    sa.ForeignKeyConstraint(['source_vertex_id'], ['vertex.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_edge_created'), 'edge', ['created'], unique=False)
    op.create_index(op.f('ix_edge_id'), 'edge', ['id'], unique=False)
    op.create_index(op.f('ix_edge_is_deleted'), 'edge', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_edge_modified'), 'edge', ['modified'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_edge_modified'), table_name='edge')
    op.drop_index(op.f('ix_edge_is_deleted'), table_name='edge')
    op.drop_index(op.f('ix_edge_id'), table_name='edge')
    op.drop_index(op.f('ix_edge_created'), table_name='edge')
    op.drop_table('edge')
    op.drop_index(op.f('ix_vertex_modified'), table_name='vertex')
    op.drop_index(op.f('ix_vertex_is_deleted'), table_name='vertex')
    op.drop_index(op.f('ix_vertex_id'), table_name='vertex')
    op.drop_index(op.f('ix_vertex_created'), table_name='vertex')
    op.drop_table('vertex')
    # ### end Alembic commands ###
