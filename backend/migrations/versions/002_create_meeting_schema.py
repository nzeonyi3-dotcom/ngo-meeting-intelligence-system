"""Alembic migration: Create meeting management schema."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Create meeting management tables."""
    
    # Create ENUM types
    op.execute("""
        CREATE TYPE meeting_category AS ENUM (
            'strategic', 'operational', 'training', 'coordination', 'other'
        )
    """)
    op.execute("""
        CREATE TYPE meeting_type AS ENUM (
            'in_person', 'virtual', 'hybrid'
        )
    """)
    op.execute("""
        CREATE TYPE meeting_status AS ENUM (
            'scheduled', 'in_progress', 'completed', 'cancelled', 'postponed'
        )
    """)
    op.execute("""
        CREATE TYPE participant_role AS ENUM (
            'chairperson', 'presenter', 'participant', 'observer', 'recorder'
        )
    """)
    op.execute("""
        CREATE TYPE recurrence_frequency AS ENUM (
            'daily', 'weekly', 'biweekly', 'monthly', 'quarterly', 'annually'
        )
    """)
    
    # Create meetings table
    op.create_table(
        'meetings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('meeting_category', sa.Enum('strategic', 'operational', 'training', 'coordination', 'other', name='meeting_category'), nullable=False),
        sa.Column('program_area', sa.String(255), nullable=False),
        sa.Column('meeting_type', sa.Enum('in_person', 'virtual', 'hybrid', name='meeting_type'), nullable=False),
        sa.Column('meeting_date', sa.DateTime(), nullable=False),
        sa.Column('start_time', sa.String(8), nullable=False),
        sa.Column('end_time', sa.String(8), nullable=False),
        sa.Column('timezone', sa.String(63), nullable=False),
        sa.Column('venue', sa.String(255), nullable=True),
        sa.Column('google_meet_link', sa.String(512), nullable=True),
        sa.Column('chairperson', sa.String(255), nullable=True),
        sa.Column('presenter', sa.String(255), nullable=True),
        sa.Column('si_counterpart', sa.String(255), nullable=True),
        sa.Column('program_lead', sa.String(255), nullable=True),
        sa.Column('supervisor', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('scheduled', 'in_progress', 'completed', 'cancelled', 'postponed', name='meeting_status'), nullable=False),
        sa.Column('is_recurring', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meetings_title'), 'meetings', ['title'], unique=False)
    op.create_index(op.f('ix_meetings_program_area'), 'meetings', ['program_area'], unique=False)
    op.create_index(op.f('ix_meetings_meeting_date'), 'meetings', ['meeting_date'], unique=False)
    op.create_index(op.f('ix_meetings_status'), 'meetings', ['status'], unique=False)
    op.create_index(op.f('ix_meetings_is_active'), 'meetings', ['is_active'], unique=False)
    
    # Create meeting_participants table
    op.create_table(
        'meeting_participants',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('meeting_id', sa.String(36), nullable=False),
        sa.Column('staff_id', sa.String(36), nullable=False),
        sa.Column('role', sa.Enum('chairperson', 'presenter', 'participant', 'observer', 'recorder', name='participant_role'), nullable=False),
        sa.Column('attendance_required', sa.Boolean(), nullable=False),
        sa.Column('presentation_required', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_participants_meeting_id'), 'meeting_participants', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_participants_staff_id'), 'meeting_participants', ['staff_id'], unique=False)
    op.create_index(op.f('ix_meeting_participants_role'), 'meeting_participants', ['role'], unique=False)
    op.create_index(op.f('ix_meeting_participants_is_active'), 'meeting_participants', ['is_active'], unique=False)
    
    # Create meeting_agenda table
    op.create_table(
        'meeting_agenda',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('meeting_id', sa.String(36), nullable=False),
        sa.Column('agenda_order', sa.Integer(), nullable=False),
        sa.Column('topic', sa.String(255), nullable=False),
        sa.Column('owner', sa.String(255), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_agenda_meeting_id'), 'meeting_agenda', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_agenda_topic'), 'meeting_agenda', ['topic'], unique=False)
    op.create_index(op.f('ix_meeting_agenda_is_active'), 'meeting_agenda', ['is_active'], unique=False)
    
    # Create meeting_attachments table
    op.create_table(
        'meeting_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('meeting_id', sa.String(36), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('storage_path', sa.String(512), nullable=False),
        sa.Column('uploaded_by', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_attachments_meeting_id'), 'meeting_attachments', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_attachments_is_active'), 'meeting_attachments', ['is_active'], unique=False)
    
    # Create meeting_recurrence table
    op.create_table(
        'meeting_recurrence',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('meeting_id', sa.String(36), nullable=False),
        sa.Column('frequency', sa.Enum('daily', 'weekly', 'biweekly', 'monthly', 'quarterly', 'annually', name='recurrence_frequency'), nullable=False),
        sa.Column('interval', sa.Integer(), nullable=False),
        sa.Column('days_of_week', sa.String(13), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('meeting_id', name='uq_meeting_recurrence_meeting_id')
    )
    op.create_index(op.f('ix_meeting_recurrence_meeting_id'), 'meeting_recurrence', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_recurrence_is_active'), 'meeting_recurrence', ['is_active'], unique=False)

def downgrade() -> None:
    """Drop meeting management tables."""
    op.drop_table('meeting_recurrence')
    op.drop_table('meeting_attachments')
    op.drop_table('meeting_agenda')
    op.drop_table('meeting_participants')
    op.drop_table('meetings')
    
    # Drop ENUM types
    op.execute('DROP TYPE recurrence_frequency')
    op.execute('DROP TYPE participant_role')
    op.execute('DROP TYPE meeting_status')
    op.execute('DROP TYPE meeting_type')
    op.execute('DROP TYPE meeting_category')
