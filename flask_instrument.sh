opentelemetry-instrument --traces_exporter otlp,console --service_name MyFlaskAppInProductionAuto --exporter_otlp_endpoint http://localhost:4317 python3 ${1:-flask_base.py}
