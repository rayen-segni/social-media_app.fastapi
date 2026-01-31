"""create posts table

Revision ID: 995645a8c679
Revises: 4b537867a3fc
Create Date: 2026-01-30 16:49:31.855413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995645a8c679'
down_revision = '4b537867a3fc'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('posts',
                sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                sa.Column("title", sa.String(), nullable=False),
                sa.Column("content", sa.String(), nullable=False),
                sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
                sa.Column("owner_id", sa.Integer(), nullable=False),
                sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
                sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete="CASCADE")
  )


def downgrade():
    op.drop_table('posts')
