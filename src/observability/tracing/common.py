import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Custom JSON Exporter


class JSONExporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def export(self, spans):
        # Serialize spans to JSON and write to file
        traces = []
        for span in spans:
            traces.append({
                "name": span.name,
                "context": {
                    "trace_id": str(span.context.trace_id),
                    "span_id": str(span.context.span_id),
                },
                "attributes": span.attributes,
                "start_time": span.start_time,
                "end_time": span.end_time,
            })
        with open(self.file_path, "w") as f:
            json.dump(traces, f, indent=4)

    def shutdown(self):
        pass


def start(
    fname: str,
    name: str = 'default'
):
    # Initialize the tracer provider
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    # Configure exporters
    json_exporter = JSONExporter(fname)
    span_processor = SimpleSpanProcessor(json_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
