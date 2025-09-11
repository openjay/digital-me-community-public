"""
Digital Me Community Edition SDK

A Python framework for building and deploying AI agent plugins on the Digital Me platform.

This is the Community Edition of the Digital Me SDK, providing:
- Plugin development framework
- Basic orchestration capabilities
- Multi-LLM provider support
- Development tools and utilities

For enterprise features, see Digital Me Enterprise Edition.
"""

__version__ = "1.0.0"
__author__ = "Digital Me Community Contributors"
__email__ = "community@yourorg.com"

from .core.agent_builder import AgentBuilder
from .core.sdk import DigitalMeSDK
from .plugins.base import BasePlugin
from .plugins.lifecycle import PluginLifecycle

__all__ = [
    "DigitalMeSDK",
    "AgentBuilder",
    "BasePlugin",
    "PluginLifecycle",
]
