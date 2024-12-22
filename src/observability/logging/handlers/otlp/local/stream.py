"""Stream based log handlers capable of OTLP data."""

import logging

from observability.logging.handlers.otlp.base import BaseJsonHandler


class OTLPStreamHandler(BaseJsonHandler):
    def __init__(self):
        handler = logging.StreamHandler()
        super().__init__(handler)
