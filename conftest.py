import logging


def pytest_configure() -> None:
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
