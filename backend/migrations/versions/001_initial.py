"""Initial migration."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade database schema."""
    # Create initial tables if needed
    pass

def downgrade() -> None:
    """Downgrade database schema."""
    pass
