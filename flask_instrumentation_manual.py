
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from flask import Flask


resource = Resource(attributes={
    SERVICE_NAME: 'MyFlaskAppInProduction'
})
provider = TracerProvider(resource=resource)
processor_console = BatchSpanProcessor(ConsoleSpanExporter())
processor_grpc = BatchSpanProcessor(OTLPSpanExporter(endpoint='http://0.0.0.0:4317'))
provider.add_span_processor(processor_console)
provider.add_span_processor(processor_grpc)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route('/')
def hello():
    with tracer.start_as_current_span('parent') as parent:
        with tracer.start_as_current_span('child') as child:
            return 'Hello, World! from our Manually Instrumented Flask App\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)