"""Base log handlers capable of OTLP data."""

import logging

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider

from observability.common.config import ObservabilityConfig
from observability.logging.record_processor.json import JsonExporterHandlerAdapter


class BaseOTLPHandler(LoggingHandler, ObservabilityConfig):
    """Base.

    """

    self._logger_provider = None

    def __init__(
        self,
        service_name: str = None,
        instance_id: str = None,
    ) -> None:
        """Registers the log provider.
        
        :param service_name: name of the process
        :param instance_id: host name
        """

        ObservabilityConfig.__init__(
            self,
            service_name=service_name,
            instance_id=instance_id,
        )

        logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": self.service_name,
                    "service.instance.id": self.instance_id,
                }
            ),
        )
        logger_provider.add_log_record_processor(
            SimpleLogRecordProcessor(
                JsonExporterHandlerAdapter(handler)))

        # Needed so that emit() will work.
        set_logger_provider(logger_provider)

        # trace_provider = TracerProvider()

        LoggingHandler.__init__(
            self,
            level=logging.NOTSET,
            logger_provider=logger_provider
        )

        self._logger_provider = logger_provider
