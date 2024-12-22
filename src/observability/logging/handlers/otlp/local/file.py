"""File based log handlers capable of OTLP data."""

import logging
from logging.handlers import WatchedFileHandler as STDLibWatchedFileHandler


from observability.logging.handlers.otlp.base import BaseJsonHandler


class WatchedFileHandler(BaseJsonHandler):
    """OTLP logs output as json."""

    def __init__(
        self,
        filename: str,
        service_name: str = None,
        instance_id: str = None,
    ) -> None:
        super().__init__(
            STDLibWatchedFileHandler(filename),
            service_name=service_name,
            instance_id=instance_id
        )
