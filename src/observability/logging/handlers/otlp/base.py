"""Base log handlers capable of OTLP data."""

import logging

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk._logs.export import (
    SimpleLogRecordProcessor,
)

from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import (
    get_logger_provider,
    set_logger_provider,
)

from observability.logging.filters.otlp import JSONNLFormatter
from observability.common.record_processor import JsonExporterHandlerAdapter
from observability.common.config import ObservabilityConfig


class BaseOTLPHandler(LoggingHandler, ObservabilityConfig):
    """Adapts OTLP log provider to python logging handler.

    """
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
        # Needed so that emit() will work.
        set_logger_provider(logger_provider)

        # trace_provider = TracerProvider()

        LoggingHandler.__init__(
            self,
            level=logging.NOTSET,
            logger_provider=logger_provider
        )


class BaseJsonHandler(BaseOTLPHandler):
    """Connects the OTLP log provider to the handler.
    
    Converts OTLP to JSON.
    """

    def __init__(
        self,
        handler: logging.Handler,
        service_name: str = None,
        instance_id: str = None,
    ):
        self._handler = handler

        super().__init__(service_name=service_name, instance_id=instance_id)

        handler.setFormatter(JSONNLFormatter())

        get_logger_provider().add_log_record_processor(
            SimpleLogRecordProcessor(JsonExporterHandlerAdapter(handler)))
