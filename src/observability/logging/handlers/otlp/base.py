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


class BaseOTLPHandler(LoggingHandler):
    """Adapts OTLP log provider to python logging handler.

    """

    def __init__(
        self,
        config: ObservabilityConfig,
    ) -> None:
        """Registers the log provider.

        :param config: service_name and instance_id container
        """

        self.config = config

        logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": self.config.service_name,
                    "service.instance.id": self.config.instance_id,
                }
            ),
        )
        # Needed so that emit() will work.
        set_logger_provider(logger_provider)

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
        config: ObservabilityConfig,
    ):
        self._handler = handler

        super().__init__(config)

        handler.setFormatter(JSONNLFormatter())

        get_logger_provider().add_log_record_processor(
            SimpleLogRecordProcessor(JsonExporterHandlerAdapter(handler)))
