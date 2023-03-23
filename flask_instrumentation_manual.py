
from opentelemetry import trace
from opentelemetry import metrics

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from flask import Flask


COLLECTOR_ENDPOINT = 'http://0.0.0.0:4317'
MY_SERVICE = 'MyFlaskAppInProductionManual'

resource = Resource(attributes={
    SERVICE_NAME: MY_SERVICE
})
tracer_provider = TracerProvider(resource=resource)

processor_console = BatchSpanProcessor(ConsoleSpanExporter())
processor_grpc = BatchSpanProcessor(OTLPSpanExporter(endpoint=COLLECTOR_ENDPOINT))

tracer_provider.add_span_processor(processor_console)
tracer_provider.add_span_processor(processor_grpc)

trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route('/')
def hello():
    with tracer.start_as_current_span('root') as root:
        root.add_event('ROOT EVENT')
        return 'Hello, World! from our Manually Instrumented Flask App\n'


@app.route('/error')
def error():
    with tracer.start_as_current_span('root') as root:
        root.add_event('ROOT EVENT')
        1 / 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)