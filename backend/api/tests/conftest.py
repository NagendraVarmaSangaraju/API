from pathlib import Path

import pytest
import sqlalchemy
from databases import Database

from backend.db import get_database
from backend.main import app
from backend.models import metadata


@pytest.fixture(autouse=True)
def set_db():

    database_path = Path(__file__).parent.joinpath("test.db")
    database_str = f"sqlite:///{database_path}"

    def get_database_override():
        return Database(database_str, force_rollback=True)

    engine = sqlalchemy.create_engine(
        database_str, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    app.dependency_overrides[get_database] = get_database_override
    yield
    database_path.unlink()
