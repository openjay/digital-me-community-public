# SPDX-License-Identifier: Apache-2.0
"""
Plugin Base Classes and Metadata

This module provides the core abstractions for Digital Me plugins,
including the BasePlugin protocol and PluginMetadata dataclass.
"""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class PluginMetadata:
    """
    Immutable metadata for a Digital Me plugin.

    This dataclass contains all the essential information about a plugin,
    including identification, versioning, and descriptive information.

    Attributes:
        id: Unique identifier for the plugin (e.g., "hello-plugin")
        name: Human-readable name (e.g., "Hello Plugin")
        version: Semantic version (e.g., "1.0.0")
        description: Brief description of what the plugin does
        author: Plugin author or organization
        license: License under which the plugin is distributed
        tags: Optional list of tags for categorization
        capabilities: Optional dict of plugin capabilities
        config_schema: Optional JSON schema for plugin configuration
    """

    id: str
    name: str
    version: str
    description: str = ""
    author: str = "community"
    license: str = "Apache-2.0"
    tags: list[str] | None = None
    capabilities: dict[str, Any] | None = None
    config_schema: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Validate metadata after initialization."""
        if not self.id:
            raise ValueError("Plugin ID cannot be empty")
        if not self.name:
            raise ValueError("Plugin name cannot be empty")
        if not self.version:
            raise ValueError("Plugin version cannot be empty")

        # Ensure tags is a list if provided
        if self.tags is not None and not isinstance(self.tags, list):
            raise ValueError("Tags must be a list of strings")


class BasePlugin(Protocol):
    """
    Protocol defining the minimal lifecycle interface all plugins must implement.

    This protocol ensures that all plugins can be managed consistently by the SDK,
    providing a standard lifecycle with initialization, startup, shutdown, and
    health checking capabilities.

    Plugins should implement this protocol by creating a class with the required
    attributes and methods. The SDK will use these methods to manage the plugin
    lifecycle automatically.
    """

    # Required metadata
    meta: PluginMetadata

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """
        Initialize the plugin with optional configuration.

        This method is called once when the plugin is first loaded. It should
        perform any necessary setup, validate configuration, and prepare the
        plugin for operation.

        Args:
            config: Optional configuration dictionary for the plugin

        Raises:
            ValueError: If the configuration is invalid
            RuntimeError: If initialization fails
        """
        ...

    def start(self) -> None:
        """
        Start the plugin's operations.

        This method is called when the plugin should begin its main operations.
        It should start any background processes, listeners, or other long-running
        activities.

        Raises:
            RuntimeError: If the plugin cannot start or is not properly initialized
        """
        ...

    def stop(self) -> None:
        """
        Stop the plugin's operations and clean up resources.

        This method is called when the plugin should shut down gracefully.
        It should stop all background processes, close connections, and clean up
        any resources to prevent memory leaks.

        Raises:
            RuntimeError: If the plugin cannot stop gracefully
        """
        ...

    def health_check(self) -> dict[str, Any]:
        """
        Perform a health check on the plugin.

        This method should return the current status of the plugin, including
        whether it's healthy, any relevant metrics, and diagnostic information.

        Returns:
            Dictionary containing health status information. Must include:
            - "status": "healthy" | "unhealthy" | "degraded"
            - Additional plugin-specific health information

        Raises:
            RuntimeError: If the health check fails
        """
        ...


class AbstractBasePlugin:
    """
    Abstract base class providing a concrete implementation of BasePlugin.

    This class provides a foundation for plugin development with common
    functionality and state management. Plugins can inherit from this class
    to get standard lifecycle management and state tracking.

    Example:
        class MyPlugin(AbstractBasePlugin):
            def __init__(self):
                super().__init__(
                    PluginMetadata(
                        id="my-plugin",
                        name="My Plugin",
                        version="1.0.0"
                    )
                )

            def initialize(self, config=None):
                super().initialize(config)
                # Plugin-specific initialization

            def start(self):
                super().start()
                # Start plugin operations

            def stop(self):
                super().stop()
                # Stop plugin operations

            def health_check(self):
                status = super().health_check()
                # Add plugin-specific health info
                return status
    """

    def __init__(self, metadata: PluginMetadata):
        """
        Initialize the plugin with metadata.

        Args:
            metadata: Plugin metadata containing identification and configuration
        """
        self.meta = metadata
        self._initialized = False
        self._running = False
        self._start_time: str | None = None

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """
        Initialize the plugin with optional configuration.

        Args:
            config: Optional configuration dictionary

        Raises:
            ValueError: If configuration is invalid
            RuntimeError: If initialization fails
        """
        if self._initialized:
            raise RuntimeError(f"Plugin {self.meta.id} is already initialized")

        # Validate configuration if schema is provided
        if self.meta.config_schema and config:
            self._validate_config(config)

        self._initialized = True

    def start(self) -> None:
        """
        Start the plugin's operations.

        Raises:
            RuntimeError: If plugin is not initialized or already running
        """
        if not self._initialized:
            raise RuntimeError(f"Plugin {self.meta.id} must be initialized before starting")

        if self._running:
            raise RuntimeError(f"Plugin {self.meta.id} is already running")

        self._running = True
        self._start_time = self._get_current_timestamp()

    def stop(self) -> None:
        """
        Stop the plugin's operations and clean up resources.

        Raises:
            RuntimeError: If plugin is not running
        """
        if not self._running:
            raise RuntimeError(f"Plugin {self.meta.id} is not running")

        self._running = False
        self._start_time = None

    def health_check(self) -> dict[str, Any]:
        """
        Perform a health check on the plugin.

        Returns:
            Dictionary containing health status and plugin information
        """
        from datetime import datetime

        status = {
            "plugin_id": self.meta.id,
            "status": "healthy" if self._running else "stopped",
            "initialized": self._initialized,
            "running": self._running,
            "version": self.meta.version,
            "timestamp": self._get_current_timestamp(),
        }

        if self._start_time:
            status["start_time"] = self._start_time
            # Calculate uptime if running
            if self._running:
                try:
                    start_dt = datetime.fromisoformat(self._start_time.replace("Z", "+00:00"))
                    uptime = (datetime.now(start_dt.tzinfo) - start_dt).total_seconds()
                    status["uptime_seconds"] = str(uptime)
                except (ValueError, TypeError):
                    pass  # Ignore timestamp parsing errors

        return status

    def _validate_config(self, config: dict[str, Any]) -> None:
        """
        Validate plugin configuration against the schema.

        Args:
            config: Configuration to validate

        Raises:
            ValueError: If configuration is invalid
        """
        # Basic validation - in a real implementation, you might use jsonschema
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        # Additional validation can be added here based on config_schema

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime

        return datetime.now().isoformat()

    def __repr__(self) -> str:
        """String representation of the plugin."""
        return f"{self.__class__.__name__}(id='{self.meta.id}', version='{self.meta.version}')"
