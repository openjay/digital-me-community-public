# Hello Plugin - Example Plugin for Digital Me Community Edition

This is a simple example plugin that demonstrates the basic structure and functionality of a Digital Me plugin. It serves as a template for plugin development and shows how to integrate with the Digital Me Community SDK.

## Features

- **Personalized Greetings**: Generate custom greetings for users
- **Echo Service**: Echo back user input for testing
- **Health Monitoring**: Provide health status and statistics
- **LLM Integration**: Uses the stub LLM provider for enhanced responses
- **Configuration Support**: Configurable greeting templates and settings

## Quick Start

### Run the Plugin

```bash
# From the project root
python examples/hello_plugin/hello_plugin.py
```

### Expected Output

```
=== Hello Plugin Demo ===

Plugin registered: Hello Plugin v0.1.0
Plugin ID: hello-plugin

=== Testing Greeting Functionality ===
Greeting for Alice: Hello, Alice! Welcome to Digital Me Community! 🚀
  LLM enhanced: Hello! I'm a stub AI assistant. You said: 'Generate a friendly greeting for Alice'
Greeting for Bob: Hello, Bob! Welcome to Digital Me Community! 🚀
  LLM enhanced: Hello! I'm a stub AI assistant. You said: 'Generate a friendly greeting for Bob'
Greeting for Digital Me Community: Hello, Digital Me Community! Welcome to Digital Me Community! 🚀
  LLM enhanced: Hello! I'm a stub AI assistant. You said: 'Generate a friendly greeting for Digital Me Community'

=== Testing Echo Functionality ===
Echo: Hello, Digital Me!
Echo: This is a test message
Echo: Echo echo echo...

=== Health Check ===
Plugin Status: healthy
Greeting Count: 3
Last Greeting: 2024-01-15T10:30:00
Provider Status: healthy

=== Plugin Statistics ===
Total Greetings: 3
Provider Calls: 3
Uptime: 0.45 seconds

=== Stopping Plugin ===
Plugin stopped successfully!

=== SDK Information ===
SDK Name: Hello Plugin Demo
Registered Plugins: 1
Plugin IDs: ['hello-plugin']
```

## Plugin Structure

```
hello_plugin/
├── plugin.yaml          # Plugin metadata and configuration schema
├── hello_plugin.py      # Main plugin implementation
└── README.md           # This documentation
```

## Configuration

The plugin supports the following configuration options:

```yaml
greeting_template: "Hello, {name}! Welcome to Digital Me Community! 🚀"
max_greetings: 1000
enable_echo: true
enable_llm: true
```

### Configuration Options

- **greeting_template**: Template string for greeting messages (supports {name} placeholder)
- **max_greetings**: Maximum number of greetings to track (default: 1000)
- **enable_echo**: Enable/disable echo functionality (default: true)
- **enable_llm**: Enable/disable LLM provider integration (default: true)

## API Methods

### greet(name: str) -> Dict[str, Any]

Generate a personalized greeting for the given name.

**Parameters:**
- `name`: Name to greet (default: "World")

**Returns:**
- Dictionary containing greeting response with keys:
  - `greeting`: The generated greeting message
  - `name`: The name that was greeted
  - `greeting_count`: Total number of greetings generated
  - `timestamp`: ISO timestamp of the greeting
  - `plugin_id`: Plugin identifier
  - `llm_enhanced`: Whether LLM was used
  - `llm_response`: LLM-generated response (if enabled)

### echo(message: str) -> Dict[str, Any]

Echo back the provided message.

**Parameters:**
- `message`: Message to echo

**Returns:**
- Dictionary containing echo response with keys:
  - `echo`: The echoed message
  - `timestamp`: ISO timestamp
  - `plugin_id`: Plugin identifier
  - `message_length`: Length of the echoed message

### health_check() -> Dict[str, Any]

Get the current health status of the plugin.

**Returns:**
- Dictionary containing health information with keys:
  - `status`: Health status ("healthy", "unhealthy", "degraded")
  - `greeting_count`: Total greetings generated
  - `last_greeting`: Timestamp of last greeting
  - `provider_health`: Health status of the LLM provider
  - `config`: Current configuration

### get_stats() -> Dict[str, Any]

Get plugin statistics and usage information.

**Returns:**
- Dictionary containing statistics with keys:
  - `greeting_count`: Total greetings generated
  - `last_greeting`: Timestamp of last greeting
  - `uptime_seconds`: Plugin uptime
  - `provider_stats`: LLM provider statistics
  - `config`: Current configuration

## Integration with Digital Me SDK

The plugin demonstrates how to integrate with the Digital Me Community SDK:

```python
from digital_me_community import DigitalMeSDK
from examples.hello_plugin.hello_plugin import HelloPlugin

# Create SDK and plugin instances
sdk = DigitalMeSDK()
plugin = HelloPlugin()

# Initialize and register plugin
plugin.initialize(config)
sdk.register(plugin)
sdk.start(plugin.meta.id)

# Use plugin functionality
result = plugin.greet("Alice")
echo_result = plugin.echo("Hello, World!")

# Check health
health = sdk.health(plugin.meta.id)

# Stop plugin
sdk.stop(plugin.meta.id)
```

## LLM Provider Integration

The plugin integrates with the StubLLMProvider to demonstrate LLM functionality:

- **Text Completion**: Uses the provider to generate enhanced greetings
- **Health Monitoring**: Monitors provider health status
- **Statistics**: Tracks provider usage and performance

## Error Handling

The plugin includes comprehensive error handling:

- **Runtime Checks**: Ensures plugin is running before executing operations
- **Configuration Validation**: Validates configuration parameters
- **Provider Failures**: Gracefully handles LLM provider failures
- **Logging**: Comprehensive logging for debugging and monitoring

## Development

### Running Tests

```bash
# Run plugin-specific tests
pytest tests/test_hello_plugin.py -v

# Run all tests
pytest tests/ -v
```

### Code Style

The plugin follows the project's code style guidelines:

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type
```

## Extending the Plugin

This plugin serves as a template for creating more complex plugins. To extend it:

1. **Add New Methods**: Implement additional functionality methods
2. **Enhance Configuration**: Add new configuration options
3. **Integrate Services**: Connect to external APIs or services
4. **Add Persistence**: Store data in databases or files
5. **Implement Caching**: Add caching for improved performance

## Troubleshooting

### Common Issues

1. **Plugin Not Starting**: Check that all dependencies are installed
2. **LLM Provider Errors**: Verify stub provider is working correctly
3. **Configuration Issues**: Validate configuration against the schema
4. **Health Check Failures**: Check plugin state and provider health

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This plugin is licensed under the Apache 2.0 License. See the main project LICENSE file for details.

## Contributing

Contributions to this example plugin are welcome! Please see the main project's CONTRIBUTING.md for guidelines.

## Support

For questions or issues with this plugin:

- **GitHub Issues**: [Create an issue](https://github.com/YOURORG/digital-me-community/issues)
- **Discussions**: [Join the discussion](https://github.com/YOURORG/digital-me-community/discussions)
- **Documentation**: [Read the docs](https://docs.yourorg.com/digital-me-community)
