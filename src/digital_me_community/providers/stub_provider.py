# SPDX-License-Identifier: Apache-2.0
"""
Stub LLM Provider for Digital Me Community Edition.

This module provides a deterministic stub implementation of an LLM provider
for demos, testing, and CI reliability. It returns predictable responses
without making actual API calls to external services.
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class StubLLMProvider:
    """
    Deterministic provider for demos & CI reliability.

    This provider returns predictable, deterministic responses without
    making actual API calls to external LLM services. It's designed for:

    - Demo purposes (no API keys required)
    - CI/CD testing (deterministic results)
    - Development and prototyping
    - Offline testing scenarios

    Example:
        provider = StubLLMProvider()
        response = provider.complete("Hello, world!")
        print(response["reply"])  # "[stubbed reply] for: Hello, world!"
    """

    def __init__(self, name: str = "stub-llm"):
        """
        Initialize the stub LLM provider.

        Args:
            name: Name for this provider instance
        """
        self.name = name
        self._call_count = 0
        self._start_time = datetime.now()

        logger.info(f"StubLLMProvider '{name}' initialized")

    def complete(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """
        Generate a completion for the given prompt.

        Args:
            prompt: The input prompt to complete
            **kwargs: Additional parameters (ignored in stub implementation)

        Returns:
            Dictionary containing the completion response with keys:
            - "ok": Boolean indicating success
            - "prompt": Original prompt
            - "reply": Generated response
            - "model": Model name used
            - "timestamp": ISO timestamp of the response
            - "call_id": Unique identifier for this call
        """
        self._call_count += 1
        call_id = f"stub-{self._call_count:06d}"

        # Generate a deterministic response based on the prompt
        reply = self._generate_stub_response(prompt)

        response = {
            "ok": True,
            "prompt": prompt,
            "reply": reply,
            "model": "stub-model-v1",
            "timestamp": datetime.now().isoformat(),
            "call_id": call_id,
            "provider": self.name,
            "metadata": {
                "stub": True,
                "call_count": self._call_count,
                "prompt_length": len(prompt),
                "response_length": len(reply),
            },
        }

        logger.debug(f"Stub completion generated for call {call_id}")
        return response

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> dict[str, Any]:
        """
        Generate a chat completion for the given messages.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters (ignored in stub implementation)

        Returns:
            Dictionary containing the chat completion response
        """
        self._call_count += 1
        call_id = f"stub-chat-{self._call_count:06d}"

        # Extract the last user message or create a default prompt
        prompt = "Hello"
        for message in reversed(messages):
            if message.get("role") == "user":
                prompt = message.get("content", "Hello")
                break

        # Generate a response
        reply = self._generate_stub_response(prompt)

        response = {
            "ok": True,
            "messages": messages,
            "reply": reply,
            "model": "stub-chat-model-v1",
            "timestamp": datetime.now().isoformat(),
            "call_id": call_id,
            "provider": self.name,
            "metadata": {
                "stub": True,
                "call_count": self._call_count,
                "message_count": len(messages),
                "response_length": len(reply),
            },
        }

        logger.debug(f"Stub chat completion generated for call {call_id}")
        return response

    def embed(self, text: str, **kwargs: Any) -> dict[str, Any]:
        """
        Generate embeddings for the given text.

        Args:
            text: Text to generate embeddings for
            **kwargs: Additional parameters (ignored in stub implementation)

        Returns:
            Dictionary containing the embedding response
        """
        self._call_count += 1
        call_id = f"stub-embed-{self._call_count:06d}"

        # Generate deterministic embeddings based on text hash
        import hashlib

        text_hash = hashlib.md5(text.encode(), usedforsecurity=False).hexdigest()

        # Create a simple deterministic embedding vector
        embedding = [
            float(int(text_hash[i : i + 2], 16)) / 255.0
            for i in range(0, min(16, len(text_hash)), 2)
        ]
        # Pad or truncate to 384 dimensions (common embedding size)
        embedding = (embedding * 24)[:384]  # Repeat and truncate to 384

        response = {
            "ok": True,
            "text": text,
            "embedding": embedding,
            "model": "stub-embedding-model-v1",
            "timestamp": datetime.now().isoformat(),
            "call_id": call_id,
            "provider": self.name,
            "metadata": {
                "stub": True,
                "call_count": self._call_count,
                "text_length": len(text),
                "embedding_dimensions": len(embedding),
            },
        }

        logger.debug(f"Stub embedding generated for call {call_id}")
        return response

    def health_check(self) -> dict[str, Any]:
        """
        Perform a health check on the provider.

        Returns:
            Dictionary containing health status information
        """
        uptime = (datetime.now() - self._start_time).total_seconds()

        return {
            "provider": self.name,
            "status": "healthy",
            "type": "stub",
            "uptime_seconds": uptime,
            "total_calls": self._call_count,
            "timestamp": datetime.now().isoformat(),
            "capabilities": ["text_completion", "chat_completion", "text_embedding"],
        }

    def _generate_stub_response(self, prompt: str) -> str:
        """
        Generate a deterministic stub response based on the prompt.

        Args:
            prompt: Input prompt

        Returns:
            Generated response string
        """
        # Simple deterministic response generation
        prompt_lower = prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower:
            return f"Hello! I'm a stub AI assistant. You said: '{prompt}'"
        elif "weather" in prompt_lower:
            return "The weather is sunny and 72°F (stub response)"
        elif "time" in prompt_lower:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')} (stub response)"
        elif "help" in prompt_lower:
            return "I'm a stub AI assistant. I can help with basic questions (stub response)"
        elif "calculate" in prompt_lower or "math" in prompt_lower:
            return "The answer is 42 (stub response)"
        elif "joke" in prompt_lower:
            return "Why did the AI go to therapy? Because it had too many neural networks! (stub response)"
        else:
            return f"[stubbed reply] for: {prompt}"

    def get_stats(self) -> dict[str, Any]:
        """
        Get statistics about the provider's usage.

        Returns:
            Dictionary containing usage statistics
        """
        uptime = (datetime.now() - self._start_time).total_seconds()

        return {
            "provider": self.name,
            "total_calls": self._call_count,
            "uptime_seconds": uptime,
            "calls_per_minute": self._call_count / max(1, uptime / 60),
            "start_time": self._start_time.isoformat(),
            "timestamp": datetime.now().isoformat(),
        }

    def reset_stats(self) -> None:
        """Reset the provider's statistics."""
        self._call_count = 0
        self._start_time = datetime.now()
        logger.info(f"Statistics reset for StubLLMProvider '{self.name}'")

    def __repr__(self) -> str:
        """String representation of the provider."""
        return f"StubLLMProvider(name='{self.name}', calls={self._call_count})"
