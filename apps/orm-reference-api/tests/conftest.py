import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def setup_db():
    return create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture()
def db_session(setup_db):
    testing_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=setup_db
    )
    session = testing_session_local()
    yield session
    session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
