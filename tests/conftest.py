import os

import dotenv
import pytest
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


dotenv.load_dotenv()
TEST_DB_USER = os.getenv("TEST_POSTGRES_USER")
TEST_DB_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_POSTGRES_HOST")
TEST_DB_PORT = os.getenv("TEST_POSTGRES_PORT")
TEST_DB_NAME = os.getenv("TEST_POSTGRES_NAME")

# Создание тестовой БД
TEST_DATABASE_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
admin_engine = create_engine(TEST_DATABASE_URL, isolation_level="AUTOCOMMIT")
engine = create_engine(TEST_DATABASE_URL)
test_session_maker = sessionmaker(engine, autocommit=False, autoflush=False)


# Создание БД, если она не существует
def create_test_database():
    if not database_exists(engine.url):
        create_database(engine.url)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_test_database()
    # Создание таблиц и тестовых данных
    with engine.connect() as con:
        try:
            with open("alembic/db_migrations/1_init_db.sql") as file:
                q = text(file.read())
                con.execute(q)
            with open("alembic/db_migrations/2_test_data.sql") as file:
                q = text(file.read())
                con.execute(q)
        except ProgrammingError:
            print("error")
            pass

    yield
    # Удаление таблиц после тестов
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = test_session_maker(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
