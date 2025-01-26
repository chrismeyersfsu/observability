"""Exercise file backed logging"""

import json
import logging
import tempfile

from observability.logging.handlers import WatchedFileHandler
from observability.common.config import ObservabilityConfig


def test_watch_file_hander():
    """Check"""

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    with tempfile.NamedTemporaryFile() as log_file:
        logger.addHandler(WatchedFileHandler(
            log_file.name,
            ObservabilityConfig(
                service_name='foo',
                instance_id='bar',
            )
        ))

        logger.info("Hello")

        log_entry = json.loads(log_file.read())

        assert len(log_entry['resourceLogs']) == 1
        attributes = log_entry['resourceLogs'][0]['resource']['attributes']
        expected_attributes = [
            {'key': 'service.name', 'value': {'stringValue': 'foo'}},
            {'key': 'service.instance.id', 'value': {'stringValue': 'bar'}}
        ]

        for expected in expected_attributes:
            matched = any(
                attr == expected
                for attr in attributes
            )
            assert matched, f"Expected {expected} not found in attributes."
