"""Translate OTLP specific data-structures to python log handler."""

import logging
import typing

from opentelemetry.sdk._logs.export import (
    LogExporter,
    LogExportResult,
)
from opentelemetry.sdk._logs import LogData
from opentelemetry.sdk._logs.export import (
    SimpleLogRecordProcessor,
)
from opentelemetry.proto.logs.v1.logs_pb2 import (
    ResourceLogs,
)
from opentelemetry.exporter.otlp.proto.common._log_encoder import encode_logs
from opentelemetry._logs import get_logger_provider

from observability.logging.handlers.otlp.base import BaseOTLPHandler
from observability.logging.filters.otlp import JSONNLFormatter


class JsonExporterHandlerAdapter(LogExporter):
    """Bridge OTLP exporter and python handler.

    python handler
      opentelemetry processor
        opentelemetry exporter.export()
          python handler.emit()
    """

    def __init__(self, handler):
        self._handler = handler
        super().__init__()

    def _translate_data(
        self,
        data: typing.Sequence[LogData]
    ) -> typing.List[ResourceLogs]:
        return encode_logs(data)

    def export(self, batch: typing.Sequence[LogData]) -> LogExportResult:
        self._handler.emit(self._translate_data(batch))  # this is the magic
        return LogExportResult.SUCCESS

    def shutdown(self) -> None:
        pass


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
