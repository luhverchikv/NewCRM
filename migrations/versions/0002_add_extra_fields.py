"""Add extra fields to users table"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new enum value for role (manager)
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'manager'")

    # Add new columns
    op.add_column('users', sa.Column('name', sa.String, nullable=False, server_default=''))
    region_enum = sa.Enum('Minsk', 'Grodno', 'Brest', name='region_enum')
    op.add_column('users', sa.Column('region', region_enum, nullable=True))
    op.add_column('users', sa.Column('direction', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'direction')
    op.drop_column('users', 'region')
    op.drop_column('users', 'name')
    # Note: can't easily drop enum value from PostgreSQL; leave it