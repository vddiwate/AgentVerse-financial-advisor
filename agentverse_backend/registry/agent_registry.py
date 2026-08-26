"""Python decorator-based agent registration module."""

from typing import Callable, Dict, Any

class AgentRegistry:
    def __init__(self):
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    def register(self, name: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator to register a new agent node in the LangGraph workflow."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._registry[name] = func
            return func
        return decorator

    def get_agent(self, name: str) -> Callable[[Any], Any]:
        """Retrieve the registered agent node function by name."""
        if name not in self._registry:
            raise KeyError(
                f"Agent '{name}' is not registered. Registered agents: {list(self._registry.keys())}"
            )
        return self._registry[name]

    def list_agents(self) -> list:
        """List all registered agent names."""
        return list(self._registry.keys())

# Global agent registry instance
agent_registry = AgentRegistry()

def register_agent(name: str):
    """Wrapper decorator for register_agent."""
    return agent_registry.register(name)
