"""File based log handlers capable of OTLP data."""

import logging
from logging.handlers import WatchedFileHandler as STDLibWatchedFileHandler


from observability.logging.handlers.adapters.otlp import BaseJsonHandler
from observability.logging.filters.otlp import JSONNLFormatter


class WatchedFileHandler(BaseJsonHandler):
    """OTLP logs output as json."""

    def __init__(
        self,
        filename: str = None,
        service_name: str = None,
        instance_id: str = None,
    ) -> None:
        if not filename:
            raise ValueError("Expected filename, got None")
        handler = STDLibWatchedFileHandler(filename)
        handler.setFormatter(JSONNLFormatter())
        super().__init__(
            handler,
            service_name=service_name,
            instance_id=instance_id
        )
