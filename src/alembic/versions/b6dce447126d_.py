"""empty message

Revision ID: b6dce447126d
Revises: d98eded5570e
Create Date: 2025-02-04 13:04:51.390023

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6dce447126d"
down_revision = "d98eded5570e"
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.add_column("files", sa.Column("new_id", UUID(), nullable=False))

    op.execute("UPDATE files SET new_id = uuid_generate_v4();")

    op.drop_column("files", "id")

    op.alter_column("files", "new_id", new_column_name="id")

    op.create_primary_key("pk_files", "files", ["id"])


def downgrade():
    op.drop_constraint("pk_files", "files", type_="primary")

    op.add_column("files", sa.Column("old_id", sa.INTEGER(), nullable=False))

    op.execute(
        """
        WITH numbered_rows AS (
            SELECT id, row_number() OVER () as rn
            FROM files
        )
        UPDATE files SET old_id = numbered_rows.rn
        FROM numbered_rows
        WHERE files.id = numbered_rows.id;
    """
    )

    op.drop_column("files", "id")

    op.alter_column("files", "old_id", new_column_name="id")

    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
