"""Python decorator-based prompt template registration module."""

from typing import Dict

class PromptRegistry:
    def __init__(self):
        self._registry: Dict[str, str] = {}

    def register(self, name: str, default_template: str) -> None:
        """Register a default fallback system prompt template in python."""
        self._registry[name] = default_template

    def get_default_prompt(self, name: str) -> str:
        """Retrieve the default python fallback prompt by name."""
        if name not in self._registry:
            raise KeyError(
                f"Prompt '{name}' is not registered in Python. Available: {list(self._registry.keys())}"
            )
        return self._registry[name]

    def list_prompts(self) -> list:
        """List all prompt names registered in python."""
        return list(self._registry.keys())

# Global prompt registry instance
prompt_registry = PromptRegistry()

def register_prompt(name: str, default_template: str) -> None:
    """Helper function to register a prompt template."""
    prompt_registry.register(name, default_template)
