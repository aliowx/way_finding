"""switch to using the SQLAlchemy v2 column type for all models

Revision ID: 043a8a745f8e
Revises: 5d05055a46a3
Create Date: 2024-01-10 11:10:19.509150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '043a8a745f8e'
down_revision = '5d05055a46a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
