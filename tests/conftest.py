"""Pytest configuration settings."""


def pytest_configure(config):
    """Add end to end marker for integration tests."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
