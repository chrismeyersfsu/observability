"""Base log handlers capable of OTLP data."""

import logging

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider

from observability.common.config import ObservabilityConfig


class BaseOTLPHandler(LoggingHandler, ObservabilityConfig):
    """Base.

    """
    def __init__(
        self,
        service_name: str = None,
        instance_name: str = None,
    ) -> None:
        """Registers the log provider.
        
        :param service_name: name of the process
        :param instance_id: host name
        """

        super(ObservabilityConfig, self).__init__(*args, **kwargs)

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

        super(LoggingHandler, self).__init__(level=logging.NOTSET, logger_provider=logger_provider)
