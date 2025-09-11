# SPDX-License-Identifier: Apache-2.0
"""
Tests for the Hello Plugin example.

This module contains comprehensive tests for the HelloPlugin class,
including greeting functionality, echo service, and health monitoring.
"""

from datetime import datetime
from unittest.mock import patch

import pytest

from digital_me_community.sdk import DigitalMeSDK
from examples.hello_plugin.hello_plugin import HelloPlugin


class TestHelloPlugin:
    """Test cases for HelloPlugin class."""

    def test_plugin_initialization(self):
        """Test plugin initialization."""
        plugin = HelloPlugin()

        assert plugin.meta.id == "hello-plugin"
        assert plugin.meta.name == "Hello Plugin"
        assert plugin.meta.version == "0.1.0"
        assert plugin._greeting_count == 0
        assert plugin._config == {}
        assert plugin._last_greeting_time is None

    def test_plugin_initialize_default_config(self):
        """Test plugin initialization with default configuration."""
        plugin = HelloPlugin()
        plugin.initialize()

        expected_config = {
            "greeting_template": "Hello, {name}! 👋",
            "max_greetings": 1000,
            "enable_echo": True,
            "enable_llm": True,
        }

        assert plugin._config == expected_config

    def test_plugin_initialize_custom_config(self):
        """Test plugin initialization with custom configuration."""
        plugin = HelloPlugin()
        custom_config = {
            "greeting_template": "Welcome, {name}! 🎉",
            "max_greetings": 500,
            "enable_echo": False,
            "enable_llm": False,
        }

        plugin.initialize(custom_config)

        assert plugin._config["greeting_template"] == "Welcome, {name}! 🎉"
        assert plugin._config["max_greetings"] == 500
        assert plugin._config["enable_echo"] is False
        assert plugin._config["enable_llm"] is False

    def test_plugin_lifecycle(self):
        """Test plugin lifecycle management."""
        plugin = HelloPlugin()
        plugin.initialize()

        # Test start
        plugin.start()
        assert plugin._running is True

        # Test stop
        plugin.stop()
        assert plugin._running is False

    def test_plugin_lifecycle_not_initialized(self):
        """Test that plugin cannot start without initialization."""
        plugin = HelloPlugin()

        with pytest.raises(RuntimeError, match="must be initialized"):
            plugin.start()

    def test_plugin_lifecycle_already_running(self):
        """Test that plugin cannot start when already running."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        with pytest.raises(RuntimeError, match="already running"):
            plugin.start()

    def test_plugin_lifecycle_not_running(self):
        """Test that plugin cannot stop when not running."""
        plugin = HelloPlugin()
        plugin.initialize()

        with pytest.raises(RuntimeError, match="not running"):
            plugin.stop()

    def test_greet_functionality(self):
        """Test greeting functionality."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        # Test greeting with default name
        result = plugin.greet()
        assert result["greeting"] == "Hello, World! 👋"
        assert result["name"] == "World"
        assert result["greeting_count"] == 1
        assert result["plugin_id"] == "hello-plugin"
        assert "timestamp" in result
        assert plugin._greeting_count == 1
        assert plugin._last_greeting_time is not None

    def test_greet_functionality_custom_name(self):
        """Test greeting functionality with custom name."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        result = plugin.greet("Alice")
        assert result["greeting"] == "Hello, Alice! 👋"
        assert result["name"] == "Alice"
        assert result["greeting_count"] == 1

    def test_greet_functionality_custom_template(self):
        """Test greeting functionality with custom template."""
        plugin = HelloPlugin()
        plugin.initialize({"greeting_template": "Welcome, {name}! 🚀"})
        plugin.start()

        result = plugin.greet("Bob")
        assert result["greeting"] == "Welcome, Bob! 🚀"
        assert result["name"] == "Bob"

    def test_greet_functionality_not_running(self):
        """Test that greeting fails when plugin is not running."""
        plugin = HelloPlugin()
        plugin.initialize()

        with pytest.raises(RuntimeError, match="must be running"):
            plugin.greet("Alice")

    def test_greet_functionality_llm_enhanced(self):
        """Test greeting functionality with LLM enhancement."""
        plugin = HelloPlugin()
        plugin.initialize({"enable_llm": True})
        plugin.start()

        result = plugin.greet("Alice")
        assert result["llm_enhanced"] is True
        assert "llm_response" in result
        assert isinstance(result["llm_response"], str)

    def test_greet_functionality_llm_disabled(self):
        """Test greeting functionality with LLM disabled."""
        plugin = HelloPlugin()
        plugin.initialize({"enable_llm": False})
        plugin.start()

        result = plugin.greet("Alice")
        assert result["llm_enhanced"] is False
        assert "llm_response" not in result

    def test_echo_functionality(self):
        """Test echo functionality."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        message = "Hello, Digital Me!"
        result = plugin.echo(message)

        assert result["echo"] == message
        assert result["plugin_id"] == "hello-plugin"
        assert result["message_length"] == len(message)
        assert "timestamp" in result

    def test_echo_functionality_not_running(self):
        """Test that echo fails when plugin is not running."""
        plugin = HelloPlugin()
        plugin.initialize()

        with pytest.raises(RuntimeError, match="must be running"):
            plugin.echo("Hello")

    def test_echo_functionality_disabled(self):
        """Test that echo fails when disabled."""
        plugin = HelloPlugin()
        plugin.initialize({"enable_echo": False})
        plugin.start()

        with pytest.raises(RuntimeError, match="disabled"):
            plugin.echo("Hello")

    def test_health_check(self):
        """Test health check functionality."""
        plugin = HelloPlugin()
        plugin.initialize()

        # Health check when stopped
        health = plugin.health_check()
        assert health["status"] == "stopped"
        assert health["initialized"] is True
        assert health["running"] is False
        assert health["greeting_count"] == 0
        assert health["last_greeting"] is None
        assert "provider_health" in health
        assert "config" in health

        # Health check when running
        plugin.start()
        health = plugin.health_check()
        assert health["status"] == "healthy"
        assert health["running"] is True

        # Health check after greeting
        plugin.greet("Alice")
        health = plugin.health_check()
        assert health["greeting_count"] == 1
        assert health["last_greeting"] is not None

    def test_get_stats(self):
        """Test statistics functionality."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        # Generate some activity
        plugin.greet("Alice")
        plugin.greet("Bob")
        plugin.echo("Test message")

        stats = plugin.get_stats()

        assert stats["plugin_id"] == "hello-plugin"
        assert stats["greeting_count"] == 2
        assert stats["last_greeting"] is not None
        assert "uptime_seconds" in stats
        assert "provider_stats" in stats
        assert "config" in stats

    def test_provider_integration(self):
        """Test LLM provider integration."""
        plugin = HelloPlugin()
        plugin.initialize()

        # Test provider health
        provider_health = plugin._provider.health_check()
        assert provider_health["status"] == "healthy"
        assert provider_health["provider"] == "hello-plugin-provider"
        assert "capabilities" in provider_health

        # Test provider completion
        result = plugin._provider.complete("Hello, world!")
        assert result["ok"] is True
        assert "reply" in result
        assert result["provider"] == "hello-plugin-provider"

    def test_provider_error_handling(self):
        """Test provider error handling."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        # Mock provider to raise an exception
        with patch.object(plugin._provider, "complete", side_effect=Exception("Provider error")):
            result = plugin.greet("Alice")

            # Should still work but without LLM enhancement
            assert result["greeting"] == "Hello, Alice! 👋"
            assert result["llm_enhanced"] is False
            assert "llm_response" not in result

    def test_plugin_with_sdk(self):
        """Test plugin integration with SDK."""
        sdk = DigitalMeSDK("Test SDK")
        plugin = HelloPlugin()

        # Initialize and register plugin
        plugin.initialize()
        sdk.register(plugin)

        # Start plugin
        sdk.start(plugin.meta.id)
        assert sdk.is_running(plugin.meta.id)

        # Test plugin functionality
        result = plugin.greet("Alice")
        assert result["greeting"] == "Hello, Alice! 👋"

        # Test health check through SDK
        health = sdk.health(plugin.meta.id)
        assert health["status"] == "healthy"
        assert health["greeting_count"] == 1

        # Stop plugin
        sdk.stop(plugin.meta.id)
        assert not sdk.is_running(plugin.meta.id)

    def test_plugin_metadata(self):
        """Test plugin metadata."""
        plugin = HelloPlugin()

        assert plugin.meta.id == "hello-plugin"
        assert plugin.meta.name == "Hello Plugin"
        assert plugin.meta.version == "0.1.0"
        assert plugin.meta.description == "Greets and echoes via stub provider"
        assert plugin.meta.author == "Digital Me Community"
        assert plugin.meta.license == "Apache-2.0"
        assert "example" in plugin.meta.tags
        assert "hello-world" in plugin.meta.tags
        assert "demo" in plugin.meta.tags

    def test_plugin_capabilities(self):
        """Test plugin capabilities."""
        plugin = HelloPlugin()

        capabilities = plugin.meta.capabilities
        assert "greeting" in capabilities
        assert "echo" in capabilities
        assert "health" in capabilities
        assert capabilities["greeting"] == "Generate personalized greetings"
        assert capabilities["echo"] == "Echo back user input"
        assert capabilities["health"] == "Provide health status information"

    def test_plugin_repr(self):
        """Test plugin string representation."""
        plugin = HelloPlugin()

        repr_str = repr(plugin)
        assert "HelloPlugin" in repr_str
        assert "hello-plugin" in repr_str
        assert "0.1.0" in repr_str

    def test_greeting_count_tracking(self):
        """Test that greeting count is properly tracked."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        # Initial count should be 0
        assert plugin._greeting_count == 0

        # Generate greetings
        plugin.greet("Alice")
        assert plugin._greeting_count == 1

        plugin.greet("Bob")
        assert plugin._greeting_count == 2

        plugin.greet("Charlie")
        assert plugin._greeting_count == 3

        # Check stats
        stats = plugin.get_stats()
        assert stats["greeting_count"] == 3

    def test_last_greeting_tracking(self):
        """Test that last greeting time is properly tracked."""
        plugin = HelloPlugin()
        plugin.initialize()
        plugin.start()

        # Initial state
        assert plugin._last_greeting_time is None

        # Generate greeting
        before_greeting = datetime.now()
        plugin.greet("Alice")
        after_greeting = datetime.now()

        # Check that timestamp is set and within expected range
        assert plugin._last_greeting_time is not None
        greeting_time = datetime.fromisoformat(plugin._last_greeting_time)
        assert before_greeting <= greeting_time <= after_greeting

        # Check health
        health = plugin.health_check()
        assert health["last_greeting"] == plugin._last_greeting_time
