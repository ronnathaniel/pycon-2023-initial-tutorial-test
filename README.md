# PyCon


## Step 1

Clone the OpenTelemetry Collector

```bash
git clone https://github.com/open-telemetry/opentelemetry-collector-contrib.git
cd opentelemetry-collector-contrib/examples/demo
```

## Step 2

At `examples/demo`, read in order:

1) `docker-compose.yaml`
        
Bring up containers with the OpenTelemetry Collector 
and 3 observability tools (Jaeger, Zipkin, and Prometheus).

**Side Note** \
(Main difference between Jaeger and Zipkin: \
Zipkin runs as 1 single process, Including Collector, Storage, Querying Service, and UI.  
Jaeger introduced the concept of splitting into different processes, one being the Collector, another being the UI, etc. \
Can you guess why?)

2) `otel-collector-config.yaml`

Defines how we want to receive Telemetry (as OTLP GRPC requests) \
How we want to process Telemetry (in Batches)  
And how we want to export Telemetry (to Prometheus, Zipkin, and Jaeger)

3) `prometheus.yaml`

Defines where we want to gather Metrics Telemetry from (the Otel Collector)


## Step 3

(Personal Choice): Delete the `demo-client` and `demo-server` lines from `docker-compose.yaml`. 

We'll create our own services.


## Step 4

```bash
docker compose up
```


