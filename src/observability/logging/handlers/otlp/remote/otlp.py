import base64

from ..base import BaseOTLPHandler

from opentelemetry._logs import get_logger_provider

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as OTLPGrpcLogExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as OTLPHttpLogExporter

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


class OTLPRemoteServerHandler(BaseOTLPHandler):
    def __init__(self, endpoint=None, protocol='grpc', service_name=None, instance_id=None, auth=None, username=None, password=None):
        super(BaseOTLPHandler, self).__init__(service_name=None, instance_id=None)
        if not endpoint:
            raise ValueError("endpoint required")

        if auth == 'basic' and (username is None or password is None):
            raise ValueError("auth type basic requires username and passsword parameters")

        self.endpoint = endpoint

        headers = {}
        if auth == 'basic':
            secret = f'{username}:{password}'
            headers['Authorization'] = "Basic " + base64.b64encode(secret.encode()).decode()

        if protocol == 'grpc':
            otlp_exporter = OTLPGrpcLogExporter(endpoint=self.endpoint, insecure=True, headers=headers)
        elif protocol == 'http':
            otlp_exporter = OTLPHttpLogExporter(endpoint=self.endpoint, headers=headers)

        get_logger_provider().add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))