from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser):
    parser.addoption("--show-plot", action="store_true", default=False)