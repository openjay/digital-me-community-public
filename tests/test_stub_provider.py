# SPDX-License-Identifier: Apache-2.0
"""Tests for the stub provider module."""

from digital_me_community.providers.stub_provider import StubLLMProvider


class TestStubLLMProvider:
    """Test cases for StubLLMProvider."""

    def test_provider_initialization(self):
        """Test provider initialization with default name."""
        provider = StubLLMProvider()
        assert provider.name == "stub-llm"
        assert provider._call_count == 0
        assert provider._start_time is not None

    def test_provider_initialization_with_name(self):
        """Test provider initialization with custom name."""
        provider = StubLLMProvider("custom-stub")
        assert provider.name == "custom-stub"
        assert provider._call_count == 0
        assert provider._start_time is not None

    def test_complete_basic(self):
        """Test basic completion functionality."""
        provider = StubLLMProvider()
        result = provider.complete("Hello world")

        assert result["ok"] is True
        assert "prompt" in result
        assert "reply" in result
        assert result["prompt"] == "Hello world"
        assert isinstance(result["reply"], str)
        assert result["model"] == "stub-model-v1"
        assert "call_id" in result
        assert "timestamp" in result
        assert "metadata" in result

    def test_complete_with_kwargs(self):
        """Test completion with additional kwargs."""
        provider = StubLLMProvider()
        result = provider.complete(
            "Test prompt", max_tokens=100, temperature=0.7, model="test-model"
        )

        assert result["ok"] is True
        assert result["prompt"] == "Test prompt"
        assert result["model"] == "stub-model-v1"  # Always uses stub model
        assert "metadata" in result
        assert result["metadata"]["stub"] is True

    def test_complete_deterministic_responses(self):
        """Test that responses are deterministic for same prompts."""
        provider = StubLLMProvider()

        result1 = provider.complete("Hello")
        result2 = provider.complete("Hello")

        # Should be deterministic for same prompt
        assert result1["reply"] == result2["reply"]

    def test_complete_different_prompts(self):
        """Test different responses for different prompts."""
        provider = StubLLMProvider()

        result1 = provider.complete("Hello")
        result2 = provider.complete("Weather")

        # Should be different for different prompts
        assert result1["reply"] != result2["reply"]

    def test_complete_call_counting(self):
        """Test that call count is incremented."""
        provider = StubLLMProvider()

        assert provider._call_count == 0
        provider.complete("Test 1")
        assert provider._call_count == 1
        provider.complete("Test 2")
        assert provider._call_count == 2

    def test_chat_basic(self):
        """Test basic chat completion functionality."""
        provider = StubLLMProvider()
        messages = [{"role": "user", "content": "Hello"}]

        result = provider.chat(messages)

        assert result["ok"] is True
        assert "messages" in result
        assert "reply" in result
        assert result["model"] == "stub-chat-model-v1"
        assert "call_id" in result
        assert "timestamp" in result
        assert "metadata" in result

    def test_chat_multiple_messages(self):
        """Test chat with multiple messages."""
        provider = StubLLMProvider()
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]

        result = provider.chat(messages)

        assert result["ok"] is True
        assert result["messages"] == messages
        assert "reply" in result
        assert result["metadata"]["message_count"] == 3

    def test_embed_basic(self):
        """Test basic embedding functionality."""
        provider = StubLLMProvider()

        result = provider.embed("Test text")

        assert result["ok"] is True
        assert "embedding" in result
        assert isinstance(result["embedding"], list)
        assert len(result["embedding"]) == 192  # Actual dimension from implementation
        assert result["model"] == "stub-embedding-model-v1"
        assert "call_id" in result
        assert "timestamp" in result
        assert "metadata" in result

    def test_embed_deterministic(self):
        """Test that embeddings are deterministic for same text."""
        provider = StubLLMProvider()

        result1 = provider.embed("Same text")
        result2 = provider.embed("Same text")

        assert result1["embedding"] == result2["embedding"]

    def test_embed_different_texts(self):
        """Test different embeddings for different texts."""
        provider = StubLLMProvider()

        result1 = provider.embed("Text 1")
        result2 = provider.embed("Text 2")

        assert result1["embedding"] != result2["embedding"]

    def test_get_stats(self):
        """Test getting usage statistics."""
        provider = StubLLMProvider()

        # Make some calls
        provider.complete("Test 1")
        provider.complete("Test 2")
        provider.embed("Test text")

        stats = provider.get_stats()

        assert "provider" in stats
        assert "total_calls" in stats
        assert "uptime_seconds" in stats
        assert "calls_per_minute" in stats
        assert "start_time" in stats
        assert "timestamp" in stats
        assert stats["total_calls"] >= 3
        assert stats["provider"] == "stub-llm"

    def test_reset_stats(self):
        """Test resetting usage statistics."""
        provider = StubLLMProvider()

        # Make some calls
        provider.complete("Test")
        provider.embed("Test")

        # Reset stats
        provider.reset_stats()

        assert provider._call_count == 0
        stats = provider.get_stats()
        assert stats["total_calls"] == 0

    def test_health_check(self):
        """Test health check functionality."""
        provider = StubLLMProvider()

        health = provider.health_check()

        assert "provider" in health
        assert "status" in health
        assert "type" in health
        assert "uptime_seconds" in health
        assert "total_calls" in health
        assert "timestamp" in health
        assert "capabilities" in health
        assert health["status"] == "healthy"
        assert health["type"] == "stub"
        assert health["provider"] == "stub-llm"
        assert "text_completion" in health["capabilities"]
        assert "chat_completion" in health["capabilities"]
        assert "text_embedding" in health["capabilities"]

    def test_provider_repr(self):
        """Test provider string representation."""
        provider = StubLLMProvider()
        repr_str = repr(provider)

        assert "StubLLMProvider" in repr_str
        assert "name='stub-llm'" in repr_str
        assert "calls=0" in repr_str

    def test_provider_repr_with_calls(self):
        """Test provider string representation with calls."""
        provider = StubLLMProvider("test-provider")
        provider.complete("Test")
        provider.complete("Test 2")

        repr_str = repr(provider)

        assert "StubLLMProvider" in repr_str
        assert "name='test-provider'" in repr_str
        assert "calls=2" in repr_str

    def test_stub_response_generation(self):
        """Test different stub response patterns."""
        provider = StubLLMProvider()

        # Test hello response
        result = provider.complete("Hello")
        assert "Hello! I'm a stub AI assistant" in result["reply"]

        # Test weather response
        result = provider.complete("What's the weather?")
        assert "sunny and 72°F" in result["reply"]

        # Test time response
        result = provider.complete("What time is it?")
        assert "current time is" in result["reply"]

        # Test help response
        result = provider.complete("Help me")
        assert "stub AI assistant" in result["reply"]

        # Test math response
        result = provider.complete("Calculate 2+2")
        assert "answer is 42" in result["reply"]

        # Test joke response
        result = provider.complete("Tell me a joke")
        assert "neural networks" in result["reply"]

        # Test default response
        result = provider.complete("Random text")
        assert "[stubbed reply] for: Random text" in result["reply"]
