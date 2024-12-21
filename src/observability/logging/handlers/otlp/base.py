"""Base log handlers capable of OTLP data."""

import sys
import os
import logging

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider


class BaseOTLPHandler(LoggingHandler):
    """Base.

    """
    def __init__(self, service_name: str = None, instance_id=None):
        """Properties that will be added to every log message.

        :param service_name: _description_, defaults to None
        :param instance_id: _description_, defaults to None
        """
        self.service_name = service_name or self.generate_service_name()
        self.instance_id = instance_id or os.uname().nodename

        logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": self.service_name,
                    "service.instance.id": self.instance_id,
                }
            ),
        )
        # Needed so that emit() will work.
        set_logger_provider(logger_provider)

        # trace_provider = TracerProvider()

        super().__init__(level=logging.NOTSET, logger_provider=logger_provider)

    def get_service_name(self):
        """Getter for service_name property."""

        return self.service_name

    def generate_service_name(self):
        """Create service name from process name."""

        # TODO: Push the service name down
        return sys.argv[1] if len(sys.argv) > 1 else (
            sys.argv[0] or 'unknown_service')
