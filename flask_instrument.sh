opentelemetry-instrument \
    --traces_exporter otlp \
    --service_name MyFlaskAppInProductionAuto \
    --exporter_otlp_endpoint http://0.0.0.0:4317 \
    python ${1:-flask_bare.py}