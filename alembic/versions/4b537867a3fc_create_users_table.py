"""create users table

Revision ID: 4b537867a3fc
Revises: 
Create Date: 2026-01-30 16:41:58.637020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b537867a3fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('users',
                  sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                  sa.Column("email", sa.String(), nullable=False, unique=True),
                  sa.Column("password", sa.String(), nullable=False),
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False)
  )


def downgrade():
    op.drop_table('users')
