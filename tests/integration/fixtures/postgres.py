import pytest
from testcontainers.postgres import PostgresContainer


def _postgresql_url_to_asyncpg(url: str) -> str:
    if "+asyncpg" in url:
        return url
    if "://" not in url:
        return url
    scheme, rest = url.split("://", 1)
    if scheme == "postgresql":
        return f"postgresql+asyncpg://{rest}"
    if scheme.startswith("postgresql+"):
        return f"postgresql+asyncpg://{rest}"
    return url


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    container = PostgresContainer("postgres:16-alpine")
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def postgres_async_database_url(postgres_container: PostgresContainer) -> str:
    return _postgresql_url_to_asyncpg(postgres_container.get_connection_url())
