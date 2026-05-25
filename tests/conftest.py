pytest_plugins = (
    "tests.integration.fixtures.postgres",
    "tests.integration.fixtures.analysis_result_repository",
    "tests.integration.infrastructure.fixtures",
    "tests.integration.application.fixtures",
    "tests.unit.infrastructure.fixtures",
    "tests.unit.application.fixtures",
    "tests.unit.domain.fixtures",
)
