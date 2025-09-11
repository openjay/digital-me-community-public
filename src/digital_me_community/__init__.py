# SPDX-License-Identifier: Apache-2.0
"""
Digital Me Community Edition - SDK and Plugin Framework

This package provides the core SDK and plugin framework for building
AI agent plugins for the Digital Me platform.

Key Components:
- DigitalMeSDK: Core SDK for plugin management and execution
- BasePlugin: Abstract base class for all plugins
- PluginMetadata: Plugin information and configuration
- StubLLMProvider: Deterministic provider for demos and testing

Example Usage:
    from digital_me_community import DigitalMeSDK, BasePlugin, PluginMetadata

    class MyPlugin(BasePlugin):
        meta = PluginMetadata(
            id="my-plugin",
            name="My Plugin",
            version="1.0.0",
            description="A sample plugin"
        )

        def initialize(self, config=None):
            pass

        def start(self):
            pass

        def stop(self):
            pass

        def health_check(self):
            return {"status": "healthy"}

    # Use the plugin
    sdk = DigitalMeSDK()
    plugin = MyPlugin()
    sdk.register(plugin)
    sdk.start(plugin.meta.id)
"""

__version__ = "0.1.0"
__author__ = "Digital Me Community"
__email__ = "community@yourorg.com"
__license__ = "Apache-2.0"

from .plugin_base import BasePlugin, PluginMetadata
from .providers.stub_provider import StubLLMProvider
from .sdk import DigitalMeSDK

# Public API
__all__ = [
    "DigitalMeSDK",
    "BasePlugin",
    "PluginMetadata",
    "StubLLMProvider",
]

# Version info
__version_info__ = tuple(map(int, __version__.split(".")))
