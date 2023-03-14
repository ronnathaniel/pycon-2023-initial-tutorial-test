
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor


from flask import Flask


os.environ['OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST'] = '.*'
os.environ['OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE'] = '.*'

resource = Resource(attributes={
    SERVICE_NAME: 'MyFlaskAppInProductionContrib'
})
provider = TracerProvider(resource=resource)
processor_grpc = BatchSpanProcessor(OTLPSpanExporter(endpoint='http://0.0.0.0:4317'))
provider.add_span_processor(processor_grpc)


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, tracer_provider=provider)


@app.route('/')
def hello():
    return 'Hello, World! from our Contrib-Instrumented Flask App\n'


@app.route('/error')
def error():
    1 / 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)