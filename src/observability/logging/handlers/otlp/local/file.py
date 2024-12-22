"""File based log handlers capable of OTLP data."""

import logging
from logging.handlers import WatchedFileHandler as STDLibWatchedFileHandler


from observability.logging.handlers.adapters.otlp import BaseJsonHandler


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
        
        super().__init__(
            handler,
            service_name=service_name,
            instance_id=instance_id
        )
