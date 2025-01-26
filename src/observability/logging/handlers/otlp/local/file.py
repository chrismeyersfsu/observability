"""File based log handlers capable of OTLP data."""

import logging
from logging.handlers import WatchedFileHandler as STDLibWatchedFileHandler


from observability.logging.handlers.otlp.base import BaseJsonHandler
from observability.common.config import ObservabilityConfig


class WatchedFileHandler(BaseJsonHandler):
    """OTLP logs output as json."""

    def __init__(
        self,
        filename: str,
        config: ObservabilityConfig,
    ) -> None:
        super().__init__(
            STDLibWatchedFileHandler(filename),
            config=config,
        )
