"""Stream based log handlers capable of OTLP data."""

import logging

from .base import BaseJsonHandler

from ansible_base.lib.observability.logging.filters.otlp import JSONNLFormatter


class OTLPStreamHandler(BaseJsonHandler):
    def __init__(self):
        handler = logging.StreamHandler()
        handler.setFormatter(JSONNLFormatter())
        super().__init__(handler)
