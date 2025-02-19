# tracing.py
import inspect
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI

def init_tracer(app: FastAPI) -> None:
    """Initialize Jaeger tracer."""
    tracer_provider = TracerProvider(
        resource=Resource.create({"service.name": "a-plus-content-generator"})
    )
    
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )
    
    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(app)

def create_span(name: str):
    """Créer un décorateur pour tracer une fonction."""
    tracer = trace.get_tracer(__name__)
    
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                with tracer.start_as_current_span(name) as span:
                    return await func(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                with tracer.start_as_current_span(name) as span:
                    return func(*args, **kwargs)
        return wrapper
    return decorator