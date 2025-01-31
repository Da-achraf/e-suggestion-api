from sqlmodel import SQLModel, create_engine, MetaData, Session
from app.core.config import get_settings

# Get the database URL from settings
DATABASE_URL = get_settings().DB.URL

# Create a metadata instance
metadata = MetaData()

# Create the database engine
engine = create_engine(DATABASE_URL)

# Base class for SQLModel models
Base = SQLModel
Base.metadata = metadata


def get_session():
    with Session(engine) as session:
        yield session
