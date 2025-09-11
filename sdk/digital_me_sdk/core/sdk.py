"""
Digital Me SDK Core

The main SDK class that provides the primary interface for plugin development
and agent orchestration in the Digital Me Community Edition.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SDKConfig:
    """Configuration for the Digital Me SDK."""

    # Plugin settings
    plugin_directory: str = "plugins"
    auto_discover_plugins: bool = True

    # LLM provider settings
    default_provider: str = "openai"
    provider_config: dict[str, Any] = None

    # Orchestration settings
    max_concurrent_agents: int = 10
    health_check_interval: int = 30

    # Logging settings
    log_level: str = "INFO"
    log_file: str | None = None

    def __post_init__(self):
        if self.provider_config is None:
            self.provider_config = {}


class DigitalMeSDK:
    """
    Main SDK class for Digital Me Community Edition.

    Provides the primary interface for:
    - Plugin management and lifecycle
    - Agent orchestration
    - LLM provider integration
    - Development utilities
    """

    def __init__(self, config: SDKConfig | None = None):
        """
        Initialize the Digital Me SDK.

        Args:
            config: SDK configuration. If None, uses default configuration.
        """
        self.config = config or SDKConfig()
        self._plugins: dict[str, Any] = {}
        self._agents: dict[str, Any] = {}
        self._providers: dict[str, Any] = {}

        # Setup logging
        self._setup_logging()

        # Initialize providers
        self._initialize_providers()

        logger.info(f"Digital Me SDK initialized with config: {self.config}")

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename=self.config.log_file,
        )

    def _initialize_providers(self) -> None:
        """Initialize LLM providers."""
        # In Community Edition, we support basic providers
        # Enterprise Edition has advanced provider management
        self._providers = {
            "openai": {"type": "openai", "config": self.config.provider_config.get("openai", {})},
            "anthropic": {
                "type": "anthropic",
                "config": self.config.provider_config.get("anthropic", {}),
            },
            "local": {"type": "local", "config": self.config.provider_config.get("local", {})},
        }

        logger.info(f"Initialized providers: {list(self._providers.keys())}")

    async def register_plugin(self, plugin: Any) -> bool:
        """
        Register a plugin with the SDK.

        Args:
            plugin: Plugin instance to register

        Returns:
            True if registration successful, False otherwise
        """
        try:
            plugin_id = getattr(plugin, "plugin_id", plugin.__class__.__name__)
            self._plugins[plugin_id] = plugin

            logger.info(f"Registered plugin: {plugin_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to register plugin: {e}")
            return False

    async def unregister_plugin(self, plugin_id: str) -> bool:
        """
        Unregister a plugin from the SDK.

        Args:
            plugin_id: ID of plugin to unregister

        Returns:
            True if unregistration successful, False otherwise
        """
        try:
            if plugin_id in self._plugins:
                del self._plugins[plugin_id]
                logger.info(f"Unregistered plugin: {plugin_id}")
                return True
            else:
                logger.warning(f"Plugin not found: {plugin_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to unregister plugin: {e}")
            return False

    def list_plugins(self) -> list[str]:
        """
        List all registered plugins.

        Returns:
            List of plugin IDs
        """
        return list(self._plugins.keys())

    async def execute_plugin(self, plugin_id: str, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a plugin with given input data.

        Args:
            plugin_id: ID of plugin to execute
            input_data: Input data for the plugin

        Returns:
            Plugin execution result
        """
        try:
            if plugin_id not in self._plugins:
                raise ValueError(f"Plugin not found: {plugin_id}")

            plugin = self._plugins[plugin_id]

            # Execute plugin (Community Edition - basic execution)
            # Enterprise Edition has advanced orchestration, monitoring, etc.
            if hasattr(plugin, "execute"):
                result = await plugin.execute(input_data)
            else:
                result = {"error": "Plugin does not implement execute method"}

            logger.info(f"Executed plugin {plugin_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to execute plugin {plugin_id}: {e}")
            return {"error": str(e)}

    async def health_check(self) -> dict[str, Any]:
        """
        Perform health check on the SDK and all registered plugins.

        Returns:
            Health status information
        """
        health_status = {
            "sdk": "healthy",
            "plugins": {},
            "providers": {},
            "timestamp": asyncio.get_event_loop().time(),
        }

        # Check plugins
        for plugin_id, plugin in self._plugins.items():
            try:
                if hasattr(plugin, "health_check"):
                    plugin_health = await plugin.health_check()
                else:
                    plugin_health = "healthy"  # Assume healthy if no health check

                health_status["plugins"][plugin_id] = plugin_health

            except Exception as e:
                health_status["plugins"][plugin_id] = f"unhealthy: {e}"

        # Check providers
        for provider_id, _provider in self._providers.items():
            try:
                # Basic provider health check
                health_status["providers"][provider_id] = "healthy"
            except Exception as e:
                health_status["providers"][provider_id] = f"unhealthy: {e}"

        return health_status

    def get_version(self) -> str:
        """
        Get the SDK version.

        Returns:
            SDK version string
        """
        from .. import __version__

        return __version__

    def get_config(self) -> SDKConfig:
        """
        Get the current SDK configuration.

        Returns:
            Current SDK configuration
        """
        return self.config

    async def shutdown(self) -> None:
        """Shutdown the SDK and cleanup resources."""
        logger.info("Shutting down Digital Me SDK")

        # Cleanup plugins
        for plugin_id in list(self._plugins.keys()):
            await self.unregister_plugin(plugin_id)

        # Cleanup providers
        self._providers.clear()

        logger.info("Digital Me SDK shutdown complete")
