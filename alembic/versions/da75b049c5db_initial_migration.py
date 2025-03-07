"""initial_migration

Revision ID: da75b049c5db
Revises: 
Create Date: 2025-02-25 02:00:07.794025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel as sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'da75b049c5db'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bus',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('plants',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('bu_id', sa.Integer(), nullable=True),
    sa.Column('plant_id', sa.Integer(), nullable=True),
    sa.Column('te_id', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('account_status', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('deactivated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['bu_id'], ['bus.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('te_id')
    )
    op.create_table('ideas',
    sa.Column('submitter_id', sa.Integer(), nullable=True),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('actual_situation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.Enum('created', 'rejected', 'approved', 'assigned', 'in progress', 'implemented', 'closed', name='ideastatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['submitter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_roles',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    op.create_table('assignments',
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idea_id'], ['ideas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attachments',
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('uploaded_by', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['idea_id'], ['ideas.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('comments',
    sa.Column('commenter_id', sa.Integer(), nullable=True),
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('body', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['commenter_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idea_id'], ['ideas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating_matrices',
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('comments', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quality', sa.Integer(), nullable=False),
    sa.Column('cost_reduction', sa.Integer(), nullable=False),
    sa.Column('time_savings', sa.Integer(), nullable=False),
    sa.Column('ehs', sa.Integer(), nullable=False),
    sa.Column('initiative', sa.Integer(), nullable=False),
    sa.Column('creativity', sa.Integer(), nullable=False),
    sa.Column('transversalization', sa.Integer(), nullable=False),
    sa.Column('effectiveness', sa.Integer(), nullable=False),
    sa.Column('total_score', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idea_id'], ['ideas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teoa_reviews',
    sa.Column('idea_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idea_id'], ['ideas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignment_comments',
    sa.Column('commenter_id', sa.Integer(), nullable=True),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('body', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['commenter_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teoa_comments',
    sa.Column('commenter_id', sa.Integer(), nullable=True),
    sa.Column('teoa_review_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('body', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['commenter_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teoa_review_id'], ['teoa_reviews.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_assignments_link',
    sa.Column('assignment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('assignment_id', 'user_id')
    )
    
    # Insert initial roles with IDENTITY_INSERT ON
    op.execute('SET IDENTITY_INSERT roles ON')
    op.execute("""
        INSERT INTO roles (id, name) VALUES
        (1, 'submitter'),
        (2, 'committee'),
        (3, 'teoa'),
        (4, 'system-admin')
    """)
    op.execute('SET IDENTITY_INSERT roles OFF')
    
    # Insert initial plants with IDENTITY_INSERT ON
    op.execute('SET IDENTITY_INSERT plants ON')
    op.execute("""
        INSERT INTO plants (id, name) VALUES
        (1, 'TAC1'),
        (2, 'TAC2'),
        (3, 'TFZ'),
        (4, 'TM1')
    """)
    op.execute('SET IDENTITY_INSERT plants OFF')
    
    # Insert initial bus with IDENTITY_INSERT ON
    op.execute('SET IDENTITY_INSERT bus ON')
    op.execute("""
        INSERT INTO bus (id, name) VALUES
        (1, 'BU1'),
        (2, 'BU2'),
        (3, 'BU3'),
        (4, 'BU4')
    """)
    op.execute('SET IDENTITY_INSERT bus OFF')

    # ### end Alembic commands ###
    
    


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_assignments_link')
    op.drop_table('teoa_comments')
    op.drop_table('assignment_comments')
    op.drop_table('teoa_reviews')
    op.drop_table('rating_matrices')
    op.drop_table('comments')
    op.drop_table('attachments')
    op.drop_table('assignments')
    op.drop_table('users_roles')
    op.drop_table('ideas')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('plants')
    op.drop_table('bus')
    # ### end Alembic commands ###
