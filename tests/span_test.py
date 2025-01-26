import json
import tempfile

from opentelemetry import trace


from observability.tracing.common import start


def test_start():
    with tempfile.NamedTemporaryFile() as span_file:
        start(span_file.name)

        tracer = trace.get_tracer(__name__)

        # Start and end spans
        with tracer.start_as_current_span("example_span") as span:
            span.set_attribute("example_key", "example_value")
            span.add_event("example_event", {"event_attr": "event_value"})

        log_entry = json.loads(span_file.read())
