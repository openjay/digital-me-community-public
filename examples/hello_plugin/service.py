# SPDX-License-Identifier: Apache-2.0
"""
FastAPI service for the Hello Plugin example.

This module provides HTTP endpoints for the Hello Plugin, including
health checks, metrics, and plugin operations.
"""

import logging
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from digital_me_community.sdk import DigitalMeSDK

from .hello_plugin import HelloPlugin

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter("hello_plugin_requests_total", "Total requests", ["method", "endpoint"])
REQUEST_DURATION = Histogram("hello_plugin_request_duration_seconds", "Request duration")
GREETING_COUNT = Counter("hello_plugin_greetings_total", "Total greetings generated")

app = FastAPI(
    title="Digital Me Community - Hello Plugin",
    description="Example plugin service demonstrating SDK capabilities",
    version="0.1.0",
)

# Initialize plugin and SDK
sdk = DigitalMeSDK("Hello Plugin Service")
plugin = HelloPlugin()

# Initialize plugin
plugin.initialize(
    {
        "greeting_template": "Hello, {name}! Welcome to Digital Me Community! 🚀",
        "max_greetings": 1000,
        "enable_echo": True,
        "enable_llm": True,
    }
)

# Register and start plugin
sdk.register(plugin)
sdk.start(plugin.meta.id)

logger.info("Hello Plugin service initialized and started")


@app.get("/health")
def health() -> dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Health status information
    """
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()

    try:
        plugin_health = plugin.health_check()
        return {
            "ok": True,
            "service": "hello",
            "version": "0.1.0",
            "plugin": plugin_health,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy") from e


@app.get("/metrics")
def metrics() -> Response:
    """
    Prometheus metrics endpoint.

    Returns:
        Prometheus-formatted metrics
    """
    REQUEST_COUNT.labels(method="GET", endpoint="/metrics").inc()

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/greet")
def greet(name: str = "World") -> dict[str, Any]:
    """
    Generate a greeting.

    Args:
        name: Name to greet

    Returns:
        Greeting response
    """
    REQUEST_COUNT.labels(method="POST", endpoint="/greet").inc()

    with REQUEST_DURATION.time():
        try:
            result = plugin.greet(name)
            GREETING_COUNT.inc()
            return result
        except Exception as e:
            logger.error(f"Greeting failed: {e}")
            raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/echo")
def echo(message: str) -> dict[str, Any]:
    """
    Echo a message.

    Args:
        message: Message to echo

    Returns:
        Echo response
    """
    REQUEST_COUNT.labels(method="POST", endpoint="/echo").inc()

    with REQUEST_DURATION.time():
        try:
            return plugin.echo(message)
        except Exception as e:
            logger.error(f"Echo failed: {e}")
            raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/stats")
def stats() -> dict[str, Any]:
    """
    Get plugin statistics.

    Returns:
        Plugin statistics
    """
    REQUEST_COUNT.labels(method="GET", endpoint="/stats").inc()

    try:
        return plugin.get_stats()
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on service shutdown."""
    logger.info("Shutting down Hello Plugin service")
    sdk.stop(plugin.meta.id)
