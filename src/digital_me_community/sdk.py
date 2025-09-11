# SPDX-License-Identifier: Apache-2.0
"""
Digital Me Community SDK

This module provides the core SDK for managing and executing plugins
in the Digital Me Community Edition platform.
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

from .plugin_base import BasePlugin, PluginMetadata

logger = logging.getLogger(__name__)


class DigitalMeSDK:
    """
    Lightweight SDK for community plugins.

    This SDK provides the core functionality for managing plugins in the
    Digital Me Community Edition, including registration, lifecycle management,
    health monitoring, and execution coordination.

    Example:
        from digital_me_community import DigitalMeSDK, BasePlugin, PluginMetadata

        class MyPlugin(BasePlugin):
            meta = PluginMetadata(id="my-plugin", name="My Plugin", version="1.0.0")

            def initialize(self, config=None): pass
            def start(self): pass
            def stop(self): pass
            def health_check(self): return {"status": "healthy"}

        # Use the SDK
        sdk = DigitalMeSDK()
        plugin = MyPlugin()
        sdk.register(plugin)
        sdk.start(plugin.meta.id)
        health = sdk.health(plugin.meta.id)
        sdk.stop(plugin.meta.id)
    """

    def __init__(self, name: str = "DigitalMeSDK"):
        """
        Initialize the Digital Me SDK.

        Args:
            name: Name for this SDK instance (useful for logging and identification)
        """
        self.name = name
        self._registry: dict[str, BasePlugin] = {}
        self._start_time = datetime.now()

        logger.info(f"Digital Me SDK '{name}' initialized")

    def register(self, plugin: BasePlugin) -> None:
        """
        Register a plugin with the SDK.

        Args:
            plugin: Plugin instance to register

        Raises:
            ValueError: If plugin ID is already registered or invalid
            TypeError: If plugin doesn't implement BasePlugin protocol
        """
        if not hasattr(plugin, "meta"):
            raise TypeError("Plugin must have 'meta' attribute with PluginMetadata")

        if not isinstance(plugin.meta, PluginMetadata):
            raise TypeError("Plugin meta must be PluginMetadata instance")

        plugin_id = plugin.meta.id

        if plugin_id in self._registry:
            raise ValueError(f"Plugin with ID '{plugin_id}' is already registered")

        if not plugin_id:
            raise ValueError("Plugin ID cannot be empty")

        self._registry[plugin_id] = plugin
        logger.info(f"Plugin '{plugin.meta.name}' (ID: {plugin_id}) registered successfully")

    def unregister(self, plugin_id: str) -> None:
        """
        Unregister a plugin from the SDK.

        Args:
            plugin_id: ID of the plugin to unregister

        Raises:
            KeyError: If plugin ID is not found
            RuntimeError: If plugin is currently running
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        plugin = self._registry[plugin_id]

        # Check if plugin is running
        try:
            health = plugin.health_check()
            if health.get("running", False):
                raise RuntimeError(
                    f"Cannot unregister running plugin '{plugin_id}'. Stop it first."
                )
        except Exception as e:
            logger.warning(f"Could not check health of plugin '{plugin_id}': {e}")

        del self._registry[plugin_id]
        logger.info(f"Plugin '{plugin_id}' unregistered successfully")

    def start(self, plugin_id: str) -> None:
        """
        Start a registered plugin.

        Args:
            plugin_id: ID of the plugin to start

        Raises:
            KeyError: If plugin ID is not found
            RuntimeError: If plugin fails to start
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        plugin = self._registry[plugin_id]

        try:
            plugin.start()
            logger.info(f"Plugin '{plugin_id}' started successfully")
        except Exception as e:
            logger.error(f"Failed to start plugin '{plugin_id}': {e}")
            raise RuntimeError(f"Failed to start plugin '{plugin_id}': {e}") from e

    def stop(self, plugin_id: str) -> None:
        """
        Stop a registered plugin.

        Args:
            plugin_id: ID of the plugin to stop

        Raises:
            KeyError: If plugin ID is not found
            RuntimeError: If plugin fails to stop
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        plugin = self._registry[plugin_id]

        try:
            plugin.stop()
            logger.info(f"Plugin '{plugin_id}' stopped successfully")
        except Exception as e:
            logger.error(f"Failed to stop plugin '{plugin_id}': {e}")
            raise RuntimeError(f"Failed to stop plugin '{plugin_id}': {e}") from e

    def health(self, plugin_id: str) -> dict[str, Any]:
        """
        Get health status of a registered plugin.

        Args:
            plugin_id: ID of the plugin to check

        Returns:
            Dictionary containing health status information

        Raises:
            KeyError: If plugin ID is not found
            RuntimeError: If health check fails
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        plugin = self._registry[plugin_id]

        try:
            health_info = plugin.health_check()
            return health_info
        except Exception as e:
            logger.error(f"Health check failed for plugin '{plugin_id}': {e}")
            raise RuntimeError(f"Health check failed for plugin '{plugin_id}': {e}") from e

    def with_config(self, plugin_id: str, fn: Callable[[BasePlugin], Any]) -> Any:
        """
        Execute a function with a plugin instance.

        This method provides a safe way to interact with a plugin instance,
        ensuring proper error handling and logging.

        Args:
            plugin_id: ID of the plugin to use
            fn: Function to execute with the plugin instance

        Returns:
            Result of the function execution

        Raises:
            KeyError: If plugin ID is not found
            RuntimeError: If function execution fails
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        plugin = self._registry[plugin_id]

        try:
            return fn(plugin)
        except Exception as e:
            logger.error(f"Function execution failed for plugin '{plugin_id}': {e}")
            raise RuntimeError(f"Function execution failed for plugin '{plugin_id}': {e}") from e

    def list_plugins(self) -> dict[str, PluginMetadata]:
        """
        List all registered plugins and their metadata.

        Returns:
            Dictionary mapping plugin IDs to their metadata
        """
        return {plugin_id: plugin.meta for plugin_id, plugin in self._registry.items()}

    def get_plugin(self, plugin_id: str) -> BasePlugin | None:
        """
        Get a registered plugin instance.

        Args:
            plugin_id: ID of the plugin to retrieve

        Returns:
            Plugin instance if found, None otherwise
        """
        return self._registry.get(plugin_id)

    def is_registered(self, plugin_id: str) -> bool:
        """
        Check if a plugin is registered.

        Args:
            plugin_id: ID of the plugin to check

        Returns:
            True if plugin is registered, False otherwise
        """
        return plugin_id in self._registry

    def is_running(self, plugin_id: str) -> bool:
        """
        Check if a plugin is currently running.

        Args:
            plugin_id: ID of the plugin to check

        Returns:
            True if plugin is running, False otherwise

        Raises:
            KeyError: If plugin ID is not found
        """
        if plugin_id not in self._registry:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        try:
            health = self.health(plugin_id)
            return bool(health.get("running", False))
        except Exception:
            return False

    def start_all(self) -> dict[str, bool]:
        """
        Start all registered plugins.

        Returns:
            Dictionary mapping plugin IDs to success status
        """
        results = {}

        for plugin_id in list(self._registry.keys()):
            try:
                self.start(plugin_id)
                results[plugin_id] = True
            except Exception as e:
                logger.error(f"Failed to start plugin '{plugin_id}': {e}")
                results[plugin_id] = False

        return results

    def stop_all(self) -> dict[str, bool]:
        """
        Stop all registered plugins.

        Returns:
            Dictionary mapping plugin IDs to success status
        """
        results = {}

        for plugin_id in list(self._registry.keys()):
            try:
                self.stop(plugin_id)
                results[plugin_id] = True
            except Exception as e:
                logger.error(f"Failed to stop plugin '{plugin_id}': {e}")
                results[plugin_id] = False

        return results

    def health_all(self) -> dict[str, dict[str, Any]]:
        """
        Get health status of all registered plugins.

        Returns:
            Dictionary mapping plugin IDs to their health status
        """
        results = {}

        for plugin_id in list(self._registry.keys()):
            try:
                results[plugin_id] = self.health(plugin_id)
            except Exception as e:
                logger.error(f"Health check failed for plugin '{plugin_id}': {e}")
                results[plugin_id] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }

        return results

    def get_sdk_info(self) -> dict[str, Any]:
        """
        Get information about the SDK instance.

        Returns:
            Dictionary containing SDK information
        """
        return {
            "name": self.name,
            "version": "0.1.0",
            "start_time": self._start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self._start_time).total_seconds(),
            "registered_plugins": len(self._registry),
            "plugin_ids": list(self._registry.keys()),
            "timestamp": datetime.now().isoformat(),
        }

    def __len__(self) -> int:
        """Return the number of registered plugins."""
        return len(self._registry)

    def __contains__(self, plugin_id: str) -> bool:
        """Check if a plugin is registered."""
        return plugin_id in self._registry

    def __repr__(self) -> str:
        """String representation of the SDK."""
        return f"DigitalMeSDK(name='{self.name}', plugins={len(self._registry)})"
