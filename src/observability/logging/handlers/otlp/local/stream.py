"""Stream based log handlers capable of OTLP data."""

import logging

from observability.logging.handlers.adapters.otlp import BaseJsonHandler


class OTLPStreamHandler(BaseJsonHandler):
    def __init__(self):
        handler = logging.StreamHandler()
        super().__init__(handler)
