# SPDX-License-Identifier: Apache-2.0
"""
Hello Plugin - Example Plugin for Digital Me Community Edition

This plugin demonstrates the basic structure and functionality of a Digital Me plugin.
It provides greeting functionality and serves as a template for plugin development.

Features:
- Personalized greetings
- Echo functionality
- Health monitoring
- Configuration support
- Stub LLM integration
"""

import logging
from datetime import datetime
from typing import Any

from digital_me_community.plugin_base import AbstractBasePlugin, PluginMetadata
from digital_me_community.providers.stub_provider import StubLLMProvider
from digital_me_community.sdk import DigitalMeSDK

logger = logging.getLogger(__name__)


class HelloPlugin(AbstractBasePlugin):
    """
    Example plugin that demonstrates Digital Me Community SDK usage.

    This plugin provides:
    - Personalized greeting functionality
    - Echo service for testing
    - Health status monitoring
    - Integration with stub LLM provider
    """

    def __init__(self):
        """Initialize the Hello Plugin."""
        metadata = PluginMetadata(
            id="hello-plugin",
            name="Hello Plugin",
            version="0.1.0",
            description="Greets and echoes via stub provider",
            author="Digital Me Community",
            license="Apache-2.0",
            tags=["example", "hello-world", "demo"],
            capabilities={
                "greeting": "Generate personalized greetings",
                "echo": "Echo back user input",
                "health": "Provide health status information",
            },
        )
        super().__init__(metadata)

        # Plugin state
        self._provider = StubLLMProvider("hello-plugin-provider")
        self._greeting_count = 0
        self._config = {}
        self._last_greeting_time: str | None = None

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """
        Initialize the plugin with configuration.

        Args:
            config: Optional configuration dictionary
        """
        super().initialize(config)

        # Set default configuration
        self._config = {
            "greeting_template": "Hello, {name}! 👋",
            "max_greetings": 1000,
            "enable_echo": True,
            "enable_llm": True,
        }

        # Update with provided configuration
        if config:
            self._config.update(config)

        logger.info(f"Hello Plugin initialized with config: {self._config}")

    def start(self) -> None:
        """Start the plugin's operations."""
        super().start()
        logger.info("Hello Plugin started and ready to greet!")

    def stop(self) -> None:
        """Stop the plugin's operations."""
        super().stop()
        logger.info("Hello Plugin stopped")

    def health_check(self) -> dict[str, Any]:
        """
        Perform a health check on the plugin.

        Returns:
            Dictionary containing health status information
        """
        status = super().health_check()

        # Add plugin-specific health information
        status.update(
            {
                "greeting_count": self._greeting_count,
                "last_greeting": self._last_greeting_time,
                "provider_health": self._provider.health_check(),
                "config": self._config,
            }
        )

        return status

    def greet(self, name: str = "World") -> dict[str, Any]:
        """
        Generate a personalized greeting.

        Args:
            name: Name to greet

        Returns:
            Dictionary containing the greeting response
        """
        if not self._running:
            raise RuntimeError("Plugin must be running to greet")

        self._greeting_count += 1
        self._last_greeting_time = datetime.now().isoformat()

        # Generate greeting using template
        greeting = self._config["greeting_template"].format(name=name)

        # Use LLM provider if enabled
        llm_response = None
        if self._config.get("enable_llm", True):
            try:
                llm_response = self._provider.complete(f"Generate a friendly greeting for {name}")
            except Exception as e:
                logger.warning(f"LLM provider failed: {e}")

        response = {
            "greeting": greeting,
            "name": name,
            "greeting_count": self._greeting_count,
            "timestamp": self._last_greeting_time,
            "plugin_id": self.meta.id,
            "llm_enhanced": llm_response is not None,
        }

        if llm_response:
            response["llm_response"] = llm_response["reply"]

        logger.info(f"Generated greeting for {name}: {greeting}")
        return response

    def echo(self, message: str) -> dict[str, Any]:
        """
        Echo back the provided message.

        Args:
            message: Message to echo

        Returns:
            Dictionary containing the echo response
        """
        if not self._running:
            raise RuntimeError("Plugin must be running to echo")

        if not self._config.get("enable_echo", True):
            raise RuntimeError("Echo functionality is disabled")

        response = {
            "echo": message,
            "timestamp": datetime.now().isoformat(),
            "plugin_id": self.meta.id,
            "message_length": len(message),
        }

        logger.info(f"Echoed message: {message}")
        return response

    def get_stats(self) -> dict[str, Any]:
        """
        Get plugin statistics.

        Returns:
            Dictionary containing plugin statistics
        """
        return {
            "plugin_id": self.meta.id,
            "greeting_count": self._greeting_count,
            "last_greeting": self._last_greeting_time,
            "uptime_seconds": self.health_check().get("uptime_seconds", 0),
            "provider_stats": self._provider.get_stats(),
            "config": self._config,
        }


def main():
    """Main function to demonstrate the Hello Plugin."""
    print("=== Hello Plugin Demo ===")
    print()

    # Create SDK and plugin instances
    sdk = DigitalMeSDK("Hello Plugin Demo")
    plugin = HelloPlugin()

    # Initialize and register plugin
    plugin.initialize(
        {
            "greeting_template": "Hello, {name}! Welcome to Digital Me Community! 🚀",
            "enable_llm": True,
            "enable_echo": True,
        }
    )

    sdk.register(plugin)
    sdk.start(plugin.meta.id)

    print(f"Plugin registered: {plugin.meta.name} v{plugin.meta.version}")
    print(f"Plugin ID: {plugin.meta.id}")
    print()

    # Test greeting functionality
    print("=== Testing Greeting Functionality ===")
    test_names = ["Alice", "Bob", "Digital Me Community"]

    for name in test_names:
        try:
            result = plugin.greet(name)
            print(f"Greeting for {name}: {result['greeting']}")
            if result.get("llm_enhanced"):
                print(f"  LLM enhanced: {result['llm_response']}")
        except Exception as e:
            print(f"Error greeting {name}: {e}")

    print()

    # Test echo functionality
    print("=== Testing Echo Functionality ===")
    test_messages = ["Hello, Digital Me!", "This is a test message", "Echo echo echo..."]

    for message in test_messages:
        try:
            result = plugin.echo(message)
            print(f"Echo: {result['echo']}")
        except Exception as e:
            print(f"Error echoing '{message}': {e}")

    print()

    # Test health check
    print("=== Health Check ===")
    try:
        health = sdk.health(plugin.meta.id)
        print(f"Plugin Status: {health['status']}")
        print(f"Greeting Count: {health['greeting_count']}")
        print(f"Last Greeting: {health['last_greeting']}")
        print(f"Provider Status: {health['provider_health']['status']}")
    except Exception as e:
        print(f"Health check failed: {e}")

    print()

    # Test plugin statistics
    print("=== Plugin Statistics ===")
    try:
        stats = plugin.get_stats()
        print(f"Total Greetings: {stats['greeting_count']}")
        print(f"Provider Calls: {stats['provider_stats']['total_calls']}")
        print(f"Uptime: {stats['uptime_seconds']:.2f} seconds")
    except Exception as e:
        print(f"Stats retrieval failed: {e}")

    print()

    # Stop plugin
    print("=== Stopping Plugin ===")
    sdk.stop(plugin.meta.id)
    print("Plugin stopped successfully!")

    # Final SDK info
    print()
    print("=== SDK Information ===")
    sdk_info = sdk.get_sdk_info()
    print(f"SDK Name: {sdk_info['name']}")
    print(f"Registered Plugins: {sdk_info['registered_plugins']}")
    print(f"Plugin IDs: {sdk_info['plugin_ids']}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    main()
