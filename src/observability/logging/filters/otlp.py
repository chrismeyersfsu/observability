"""Convert from OTLP data structures to somehting more generic."""

import base64
import logging
import json

from google.protobuf import json_format


class JSONNLFormatter(logging.Formatter):
    """
    Convert OTLP data structure to json.
    
    opentelemetry.proto.collector.logs.v1.logs_service_pb2.ExportLogsServiceRequest --> json
    """

    def format(self, record):
        data = json_format.MessageToDict(record)
        d = data['resourceLogs'][0]['scopeLogs'][0]['logRecords'][0]
        if 'traceId' in d:
            d['traceId'] = base64.b64decode(d['traceId']).hex()
        if 'spanId' in d:
            d['spanId'] = base64.b64decode(d['spanId']).hex()
        return json.dumps(data)
