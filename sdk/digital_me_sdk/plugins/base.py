"""
Base Plugin Class

Provides the foundation for all Digital Me plugins in the Community Edition.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""

    name: str
    version: str
    description: str
    author: str
    license: str = "Apache-2.0"
    tags: list[str] = None
    dependencies: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []


class BasePlugin(ABC):
    """
    Base class for all Digital Me plugins.

    This is the Community Edition base class. Enterprise Edition provides
    additional features like advanced lifecycle management, monitoring,
    and enterprise security features.
    """

    def __init__(self, metadata: PluginMetadata):
        """
        Initialize the base plugin.

        Args:
            metadata: Plugin metadata
        """
        self.metadata = metadata
        self.plugin_id = f"{metadata.name}-{metadata.version}"
        self._initialized = False
        self._running = False
        self._start_time: datetime | None = None

        logger.info(f"Initialized plugin: {self.plugin_id}")

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the plugin with given input data.

        This is the main entry point for plugin execution.

        Args:
            input_data: Input data for the plugin

        Returns:
            Plugin execution result
        """
        pass

    async def initialize(self) -> bool:
        """
        Initialize the plugin.

        Override this method to perform plugin-specific initialization.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if self._initialized:
                logger.warning(f"Plugin {self.plugin_id} already initialized")
                return True

            # Plugin-specific initialization
            await self._on_initialize()

            self._initialized = True
            logger.info(f"Plugin {self.plugin_id} initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize plugin {self.plugin_id}: {e}")
            return False

    async def start(self) -> bool:
        """
        Start the plugin.

        Override this method to perform plugin-specific startup tasks.

        Returns:
            True if startup successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error(f"Plugin {self.plugin_id} not initialized")
                return False

            if self._running:
                logger.warning(f"Plugin {self.plugin_id} already running")
                return True

            # Plugin-specific startup
            await self._on_start()

            self._running = True
            self._start_time = datetime.now()
            logger.info(f"Plugin {self.plugin_id} started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start plugin {self.plugin_id}: {e}")
            return False

    async def stop(self) -> bool:
        """
        Stop the plugin.

        Override this method to perform plugin-specific shutdown tasks.

        Returns:
            True if shutdown successful, False otherwise
        """
        try:
            if not self._running:
                logger.warning(f"Plugin {self.plugin_id} not running")
                return True

            # Plugin-specific shutdown
            await self._on_stop()

            self._running = False
            self._start_time = None
            logger.info(f"Plugin {self.plugin_id} stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to stop plugin {self.plugin_id}: {e}")
            return False

    async def health_check(self) -> dict[str, Any]:
        """
        Perform health check on the plugin.

        Override this method to implement plugin-specific health checks.

        Returns:
            Health status information
        """
        try:
            health_status = {
                "plugin_id": self.plugin_id,
                "status": "healthy",
                "initialized": self._initialized,
                "running": self._running,
                "uptime": None,
                "timestamp": datetime.now().isoformat(),
            }

            if self._start_time:
                uptime = datetime.now() - self._start_time
                health_status["uptime"] = uptime.total_seconds()

            # Plugin-specific health check
            plugin_health = await self._on_health_check()
            health_status.update(plugin_health)

            return health_status

        except Exception as e:
            logger.error(f"Health check failed for plugin {self.plugin_id}: {e}")
            return {
                "plugin_id": self.plugin_id,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            Plugin metadata
        """
        return self.metadata

    def get_status(self) -> dict[str, Any]:
        """
        Get current plugin status.

        Returns:
            Current plugin status
        """
        return {
            "plugin_id": self.plugin_id,
            "initialized": self._initialized,
            "running": self._running,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "uptime": (datetime.now() - self._start_time).total_seconds()
            if self._start_time
            else 0,
        }

    # Hook methods for subclasses to override

    @abstractmethod
    async def _on_initialize(self) -> None:
        """
        Plugin-specific initialization.

        Override this method to perform plugin-specific initialization tasks.
        """
        pass

    @abstractmethod
    async def _on_start(self) -> None:
        """
        Plugin-specific startup.

        Override this method to perform plugin-specific startup tasks.
        """
        pass

    @abstractmethod
    async def _on_stop(self) -> None:
        """
        Plugin-specific shutdown.

        Override this method to perform plugin-specific shutdown tasks.
        """
        pass

    async def _on_health_check(self) -> dict[str, Any]:
        """
        Plugin-specific health check.

        Override this method to implement plugin-specific health checks.

        Returns:
            Additional health status information
        """
        return {}

    def __str__(self) -> str:
        """String representation of the plugin."""
        return f"Plugin({self.plugin_id})"

    def __repr__(self) -> str:
        """Detailed string representation of the plugin."""
        return (
            f"Plugin(id={self.plugin_id}, initialized={self._initialized}, running={self._running})"
        )
