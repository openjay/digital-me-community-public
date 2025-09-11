"""
Hello World Plugin Example

A simple example plugin that demonstrates the basic structure and functionality
of a Digital Me Community Edition plugin.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from digital_me_sdk.plugins.base import BasePlugin, PluginMetadata

logger = logging.getLogger(__name__)


class HelloWorldPlugin(BasePlugin):
    """
    A simple hello world plugin that demonstrates basic plugin functionality.

    This plugin:
    - Accepts a name parameter
    - Returns a personalized greeting
    - Demonstrates plugin lifecycle methods
    - Shows basic health checking
    """

    def __init__(self):
        """Initialize the Hello World plugin."""
        metadata = PluginMetadata(
            name="hello_world",
            version="1.0.0",
            description="A simple hello world plugin for Digital Me Community Edition",
            author="Digital Me Community",
            license="Apache-2.0",
            tags=["example", "hello", "greeting"],
            dependencies=[],
        )

        super().__init__(metadata)
        self._greeting_count = 0

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the hello world plugin.

        Args:
            input_data: Input data containing optional 'name' parameter

        Returns:
            Greeting message and metadata
        """
        try:
            # Extract name from input data
            name = input_data.get("name", "World")

            # Increment greeting counter
            self._greeting_count += 1

            # Create greeting message
            greeting = f"Hello, {name}! 👋"

            # Prepare response
            result = {
                "greeting": greeting,
                "timestamp": datetime.now().isoformat(),
                "greeting_count": self._greeting_count,
                "plugin_id": self.plugin_id,
                "input_received": input_data,
            }

            logger.info(f"Hello World plugin executed for '{name}' (count: {self._greeting_count})")
            return result

        except Exception as e:
            logger.error(f"Hello World plugin execution failed: {e}")
            return {
                "error": f"Plugin execution failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "plugin_id": self.plugin_id,
            }

    async def _on_initialize(self) -> None:
        """Plugin-specific initialization."""
        logger.info("Hello World plugin initializing...")
        self._greeting_count = 0
        logger.info("Hello World plugin initialized successfully")

    async def _on_start(self) -> None:
        """Plugin-specific startup."""
        logger.info("Hello World plugin starting...")
        # Could start background tasks, connect to services, etc.
        logger.info("Hello World plugin started successfully")

    async def _on_stop(self) -> None:
        """Plugin-specific shutdown."""
        logger.info("Hello World plugin stopping...")
        # Could stop background tasks, disconnect from services, etc.
        logger.info("Hello World plugin stopped successfully")

    async def _on_health_check(self) -> dict[str, Any]:
        """
        Plugin-specific health check.

        Returns:
            Additional health status information
        """
        return {
            "greeting_count": self._greeting_count,
            "last_greeting": datetime.now().isoformat() if self._greeting_count > 0 else None,
            "status": "healthy",
        }


# Example usage and testing
async def main():
    """Example usage of the Hello World plugin."""

    # Create plugin instance
    plugin = HelloWorldPlugin()

    # Initialize and start the plugin
    await plugin.initialize()
    await plugin.start()

    # Test plugin execution
    test_cases = [
        {"name": "Alice"},
        {"name": "Bob"},
        {},  # No name provided
        {"name": "Digital Me Community", "extra": "data"},
    ]

    print("=== Hello World Plugin Demo ===\n")

    for i, test_input in enumerate(test_cases, 1):
        print(f"Test {i}: {test_input}")
        result = await plugin.execute(test_input)
        print(f"Result: {result}\n")

    # Health check
    health = await plugin.health_check()
    print(f"Health Check: {health}\n")

    # Plugin status
    status = plugin.get_status()
    print(f"Plugin Status: {status}\n")

    # Stop the plugin
    await plugin.stop()
    print("Plugin stopped successfully!")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
