# PyCon: 
### How to Monitor and Troubleshoot Applications in Production using OpenTelemetry:




## Table of Contents
- [Pre-Reqs](#pre-requirements)
- [Step 1: Getting the Collector](#step-1)
- [Step 2: Inspecting the Source Code](#step-2)





## Pre-Requirements


> All can be installed via
> [HomeBrew](https://formulae.brew.sh/formula/)
> / Yum
> / Rpm
> / Pacman
> / Apt-Get
> / Any OS Package Manager

- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/)


## Step 1
> #### Getting the Collector

Clone the OpenTelemetry Collector. In a Terminal, run:

```bash
git clone https://github.com/open-telemetry/opentelemetry-collector-contrib.git
cp -r opentelemetry-collector-contrib/examples/demo collector-demo
cd collector-demo
```

## Step 2
> #### Inspecting the Source Code

At `collector-demo/`, read in order:

1) `docker-compose.yaml`
        
Bring up containers with the OpenTelemetry Collector 
and 3 observability tools (Jaeger, Zipkin, and Prometheus).

**Side Note** \
(Main difference between Jaeger and Zipkin: \
Zipkin runs as 1 single process, Including Collector, Storage, Querying Service, and UI.  
Jaeger introduced the concept of splitting into different processes, one being the Collector, another being the UI, etc. 

*Prompt:* Can you guess why?)



2) `otel-collector-config.yaml`

Defines how we want to receive Telemetry (as OTLP GRPC requests) \
How we want to process Telemetry (in Batches)  
And how we want to export Telemetry (to Prometheus, Zipkin, and Jaeger)

3) `prometheus.yaml`

Defines where we want to gather Metrics Telemetry from (the Otel Collector)


## Step 3
> #### Cleanup

(Personal Choice): Delete the `demo-client` and `demo-server` lines from `docker-compose.yaml`.

And the `client/` and `server/` directories.

We'll create our own services.


## Step 4
> #### Booting up the Collector 

Lets start the collector locally. In a Terminal, run:

```bash
docker compose up
```

And voila, our collector and observability tools are up and running.

## Step 5
> #### Inspecting our Toolbox

View your Observability tools at:


Jaeger = [localhost:16686](http://0.0.0.0:16686)

Zipkin = [localhost:9411](http://0.0.0.0:9411)

Prometheus = [localhost:9090](http://0.0.0.0:9090)


## Step 6
> #### The Base Case

Create a Python file (`flask_bare.py`) with the following:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World! from our plain Flask App\n'


@app.route('/error')
def error():
    1 / 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

```

And open 2 terminals side by side (`CMD + D`, move between with `CMD + [`).


In the first terminal, run with file with 

```python
python3 flask_bare.py
```

And in the second terminal, ping the server with curl 

```python
curl localhost:5000
```

for a successful response.

Then, see what happens when you 

```python
curl localhost:5000/error
```

And I want you to tell me (as the client) 
- what happened? 
- why did the request fail?
- did the server crash?
- is the server still up and running?
- is my application still working or do I need to restart it?

(Rhetorical, of course).

OpenTelemetry to the rescue!

## Step 7
> #### The Manual Instrumentation Case

Manual Instrumentation is the hardest but safest of all instrumentations. 
The developer is in complete control over what gets instrumented, and how.

Create a Python file by duplicating `flask_bare.py` with:

```bash
cp flask_bare.py flask_instrumentation_manual.py
```

and let's install our dependencies:

```bash
pip3 install \
   opentelemetry-api \
   opentelemetry-sdk  \
   opentelemetry-exporter-otlp
```

And in our `flask_instrumentation_manual.py` file add some boilerplate at the top:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


COLLECTOR_ENDPOINT = 'http://0.0.0.0:4317'
SERVICE_NAME = 'MyFlaskAppInProductionManual'

resource = Resource(attributes={
    SERVICE_NAME: SERVICE_NAME
})
provider = TracerProvider()

# exports to STDOUT
processor_console = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor_console)
# exports to otel collector at endpoint
processor_grpc = BatchSpanProcessor(OTLPSpanExporter(endpoint=COLLECTOR_ENDPOINT))
provider.add_span_processor(processor_grpc)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```

and replace our `hello()` function at `/` route with 

```python
@app.route('/')
def hello():
    with tracer.start_as_current_span("parent") as parent:
            with tracer.start_as_current_span("child") as child:
                return 'Hello, World!\n'
```

## Step 8
> #### The Contrib Instrumentation Case

Contributed packages include support for third party tools. 

Restart our instrumentation with 

```python
cp flask_bare.py flask_instrumentation_contrib.py
```

and Install the Flask contrib with:

```bash
pip3 install opentelemetry-instrumentation-flask
```


Only 2 lines are needed to instrument 



efefe

e
ge

egeg


egeg


egeg


egeg