"""Added account table

Revision ID: b8300b9777bb
Revises: 3df657518309
Create Date: 2024-10-09 08:26:58.493687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8300b9777bb'
down_revision = '3df657518309'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vertex', 'x',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('vertex', 'y',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vertex', 'y',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('vertex', 'x',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
