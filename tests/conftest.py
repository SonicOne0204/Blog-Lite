import pytest
from django.db import connection


@pytest.fixture(scope="session", autouse=True)
def close_db_connections():
    yield
    connection.close()
