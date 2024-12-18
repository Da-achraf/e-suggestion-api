from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import your SQLModel models and settings
from db.base import Base
from db.models import *
from core.config import get_settings

# This is the Alembic Config object, which provides access to the values within the .ini file.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=get_settings().DB.URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Load the database URL from the settings
    db_url = get_settings().DB.URL

    # Configure the engine using the database URL
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # Use config_ini_section instead of config_options
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=db_url,  # Pass the database URL explicitly
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()