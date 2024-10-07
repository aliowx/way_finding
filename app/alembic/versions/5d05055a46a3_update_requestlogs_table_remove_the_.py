"""Update requestlogs table: Remove the 'null=True' and 'index=True' attributes from the columns

Revision ID: 5d05055a46a3
Revises: 4747a32d83a2
Create Date: 2024-01-10 11:07:16.876482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d05055a46a3'
down_revision = '4747a32d83a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
