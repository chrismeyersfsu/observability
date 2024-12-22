"""Translate OTLP specific data-structures to python log handler."""

from observability.logging.handlers.otlp.base import BaseOTLPHandler
from opentelemetry.sdk._logs.export import (
    SimpleLogRecordProcessor,
)
from opentelemetry._logs import get_logger_provider
from observability.logging.filters.otlp import JSONNLFormatter

from observability.common.record_processor import JsonExporterHandlerAdapter


class BaseJsonHandler(BaseOTLPHandler):
    """."""

    def __init__(
        self,
        handler: logging.Handler,
        service_name: str = None,
        instance_id: str = None,
    ):
        super().__init__(service_name=service_name, instance_id=instance_id)

        handler.setFormatter(JSONNLFormatter())

        get_logger_provider().add_log_record_processor(
            SimpleLogRecordProcessor(JsonExporterHandlerAdapter(handler)))
