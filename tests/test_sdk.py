# SPDX-License-Identifier: Apache-2.0
"""
Tests for the Digital Me Community SDK.

This module contains comprehensive tests for the DigitalMeSDK class,
including plugin registration, lifecycle management, and health monitoring.
"""

from unittest.mock import Mock

import pytest

from digital_me_community.plugin_base import AbstractBasePlugin, PluginMetadata
from digital_me_community.sdk import DigitalMeSDK


class MockPlugin(AbstractBasePlugin):
    """Mock plugin for testing purposes."""

    def __init__(self, plugin_id: str = "mock", name: str = "Mock Plugin", version: str = "0.0.1"):
        metadata = PluginMetadata(
            id=plugin_id, name=name, version=version, description="Mock plugin for testing"
        )
        super().__init__(metadata)
        self.running = False
        self.initialized = False

    def initialize(self, config=None):
        self.initialized = True

    def start(self):
        if not self.initialized:
            raise RuntimeError("Plugin must be initialized before starting")
        self.running = True

    def stop(self):
        self.running = False

    def health_check(self):
        return {
            "status": "healthy" if self.running else "stopped",
            "running": self.running,
            "initialized": self.initialized,
            "plugin_id": self.meta.id,
        }


class TestDigitalMeSDK:
    """Test cases for DigitalMeSDK class."""

    def test_sdk_initialization(self):
        """Test SDK initialization."""
        sdk = DigitalMeSDK("Test SDK")
        assert sdk.name == "Test SDK"
        assert len(sdk) == 0
        assert sdk._registry == {}

    def test_plugin_registration(self):
        """Test plugin registration."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        # Register plugin
        sdk.register(plugin)
        assert len(sdk) == 1
        assert "test-plugin" in sdk
        assert sdk.is_registered("test-plugin")
        assert sdk.get_plugin("test-plugin") == plugin

    def test_plugin_registration_duplicate_id(self):
        """Test that duplicate plugin IDs are rejected."""
        sdk = DigitalMeSDK()
        plugin1 = MockPlugin("test-plugin")
        plugin2 = MockPlugin("test-plugin")

        sdk.register(plugin1)

        with pytest.raises(ValueError, match="already registered"):
            sdk.register(plugin2)

    def test_plugin_registration_invalid_plugin(self):
        """Test that invalid plugins are rejected."""
        sdk = DigitalMeSDK()

        # Plugin without meta attribute
        invalid_plugin = Mock(spec=[])  # Mock with no attributes
        with pytest.raises(TypeError, match="must have 'meta' attribute"):
            sdk.register(invalid_plugin)

    def test_plugin_registration_invalid_meta(self):
        """Test that plugins with invalid meta are rejected."""
        sdk = DigitalMeSDK()

        # Plugin with invalid meta
        invalid_plugin = Mock()
        invalid_plugin.meta = "not metadata"
        with pytest.raises(TypeError, match="must be PluginMetadata instance"):
            sdk.register(invalid_plugin)

    def test_plugin_unregistration(self):
        """Test plugin unregistration."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)
        assert len(sdk) == 1

        sdk.unregister("test-plugin")
        assert len(sdk) == 0
        assert not sdk.is_registered("test-plugin")

    def test_plugin_unregistration_not_found(self):
        """Test unregistering non-existent plugin."""
        sdk = DigitalMeSDK()

        with pytest.raises(KeyError, match="not found"):
            sdk.unregister("non-existent")

    def test_plugin_lifecycle(self):
        """Test plugin lifecycle management."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)
        plugin.initialize()

        # Start plugin
        sdk.start("test-plugin")
        assert sdk.is_running("test-plugin")
        assert plugin.running

        # Stop plugin
        sdk.stop("test-plugin")
        assert not sdk.is_running("test-plugin")
        assert not plugin.running

    def test_plugin_lifecycle_not_found(self):
        """Test lifecycle operations on non-existent plugin."""
        sdk = DigitalMeSDK()

        with pytest.raises(KeyError, match="not found"):
            sdk.start("non-existent")

        with pytest.raises(KeyError, match="not found"):
            sdk.stop("non-existent")

    def test_plugin_health_check(self):
        """Test plugin health checking."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)
        plugin.initialize()

        # Health check when stopped
        health = sdk.health("test-plugin")
        assert health["status"] == "stopped"
        assert not health["running"]

        # Health check when running
        sdk.start("test-plugin")
        health = sdk.health("test-plugin")
        assert health["status"] == "healthy"
        assert health["running"]

    def test_plugin_health_check_not_found(self):
        """Test health check on non-existent plugin."""
        sdk = DigitalMeSDK()

        with pytest.raises(KeyError, match="not found"):
            sdk.health("non-existent")

    def test_with_config(self):
        """Test with_config method."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)

        def get_plugin_name(p):
            return p.meta.name

        result = sdk.with_config("test-plugin", get_plugin_name)
        assert result == "Mock Plugin"

    def test_with_config_not_found(self):
        """Test with_config on non-existent plugin."""
        sdk = DigitalMeSDK()

        with pytest.raises(KeyError, match="not found"):
            sdk.with_config("non-existent", lambda p: p)

    def test_list_plugins(self):
        """Test listing plugins."""
        sdk = DigitalMeSDK()
        plugin1 = MockPlugin("plugin1", "Plugin 1")
        plugin2 = MockPlugin("plugin2", "Plugin 2")

        sdk.register(plugin1)
        sdk.register(plugin2)

        plugins = sdk.list_plugins()
        assert len(plugins) == 2
        assert "plugin1" in plugins
        assert "plugin2" in plugins
        assert plugins["plugin1"].name == "Plugin 1"
        assert plugins["plugin2"].name == "Plugin 2"

    def test_start_all(self):
        """Test starting all plugins."""
        sdk = DigitalMeSDK()
        plugin1 = MockPlugin("plugin1")
        plugin2 = MockPlugin("plugin2")

        sdk.register(plugin1)
        sdk.register(plugin2)

        plugin1.initialize()
        plugin2.initialize()

        results = sdk.start_all()
        assert results["plugin1"] is True
        assert results["plugin2"] is True
        assert sdk.is_running("plugin1")
        assert sdk.is_running("plugin2")

    def test_stop_all(self):
        """Test stopping all plugins."""
        sdk = DigitalMeSDK()
        plugin1 = MockPlugin("plugin1")
        plugin2 = MockPlugin("plugin2")

        sdk.register(plugin1)
        sdk.register(plugin2)

        plugin1.initialize()
        plugin2.initialize()
        sdk.start_all()

        results = sdk.stop_all()
        assert results["plugin1"] is True
        assert results["plugin2"] is True
        assert not sdk.is_running("plugin1")
        assert not sdk.is_running("plugin2")

    def test_health_all(self):
        """Test health check for all plugins."""
        sdk = DigitalMeSDK()
        plugin1 = MockPlugin("plugin1")
        plugin2 = MockPlugin("plugin2")

        sdk.register(plugin1)
        sdk.register(plugin2)

        plugin1.initialize()
        plugin2.initialize()

        health_all = sdk.health_all()
        assert "plugin1" in health_all
        assert "plugin2" in health_all
        assert health_all["plugin1"]["status"] == "stopped"
        assert health_all["plugin2"]["status"] == "stopped"

    def test_get_sdk_info(self):
        """Test getting SDK information."""
        sdk = DigitalMeSDK("Test SDK")
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)

        info = sdk.get_sdk_info()
        assert info["name"] == "Test SDK"
        assert info["version"] == "0.1.0"
        assert info["registered_plugins"] == 1
        assert "test-plugin" in info["plugin_ids"]
        assert "start_time" in info
        assert "uptime_seconds" in info

    def test_sdk_repr(self):
        """Test SDK string representation."""
        sdk = DigitalMeSDK("Test SDK")
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)

        repr_str = repr(sdk)
        assert "DigitalMeSDK" in repr_str
        assert "Test SDK" in repr_str
        assert "plugins=1" in repr_str

    def test_plugin_contains(self):
        """Test plugin containment check."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        assert "test-plugin" not in sdk

        sdk.register(plugin)
        assert "test-plugin" in sdk
        assert "non-existent" not in sdk

    def test_plugin_lifecycle_errors(self):
        """Test plugin lifecycle error handling."""
        sdk = DigitalMeSDK()

        # Create a plugin that fails to start
        class FailingPlugin(AbstractBasePlugin):
            def __init__(self):
                metadata = PluginMetadata(id="failing", name="Failing", version="1.0.0")
                super().__init__(metadata)

            def initialize(self, config=None):
                super().initialize(config)

            def start(self):
                raise RuntimeError("Start failed")

            def stop(self):
                pass

            def health_check(self):
                return {"status": "error"}

        plugin = FailingPlugin()
        sdk.register(plugin)
        plugin.initialize()

        with pytest.raises(RuntimeError, match="Failed to start"):
            sdk.start("failing")

    def test_health_check_errors(self):
        """Test health check error handling."""
        sdk = DigitalMeSDK()

        # Create a plugin that fails health checks
        class UnhealthyPlugin(AbstractBasePlugin):
            def __init__(self):
                metadata = PluginMetadata(id="unhealthy", name="Unhealthy", version="1.0.0")
                super().__init__(metadata)

            def initialize(self, config=None):
                super().initialize(config)

            def start(self):
                super().start()

            def stop(self):
                super().stop()

            def health_check(self):
                raise RuntimeError("Health check failed")

        plugin = UnhealthyPlugin()
        sdk.register(plugin)
        plugin.initialize()

        with pytest.raises(RuntimeError, match="Health check failed"):
            sdk.health("unhealthy")

    def test_with_config_errors(self):
        """Test with_config error handling."""
        sdk = DigitalMeSDK()
        plugin = MockPlugin("test-plugin")

        sdk.register(plugin)

        def failing_function(p):
            raise ValueError("Function failed")

        with pytest.raises(RuntimeError, match="Function execution failed"):
            sdk.with_config("test-plugin", failing_function)

    def test_plugin_metadata_validation_errors(self):
        """Test PluginMetadata validation error cases."""
        from digital_me_community.plugin_base import PluginMetadata

        # Test empty ID
        with pytest.raises(ValueError, match="Plugin ID cannot be empty"):
            PluginMetadata(id="", name="Test", version="1.0.0")

        # Test empty name
        with pytest.raises(ValueError, match="Plugin name cannot be empty"):
            PluginMetadata(id="test", name="", version="1.0.0")

        # Test empty version
        with pytest.raises(ValueError, match="Plugin version cannot be empty"):
            PluginMetadata(id="test", name="Test", version="")

        # Test invalid tags type
        with pytest.raises(ValueError, match="Tags must be a list of strings"):
            PluginMetadata(id="test", name="Test", version="1.0.0", tags="not-a-list")
