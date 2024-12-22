"""Stream based log handlers capable of OTLP data."""

import logging

from observability.logging.handlers.adapters.otlp import BaseJsonHandler

from ansible_base.lib.observability.logging.filters.otlp import JSONNLFormatter


class OTLPStreamHandler(BaseJsonHandler):
    def __init__(self):
        handler = logging.StreamHandler()
        super().__init__(handler)
