"""Python decorator-based tool registration module."""

from typing import Callable, Dict, Any, List

class ToolRegistry:
    def __init__(self):
        self._registry: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to register a python function as a tool in the registry."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._registry[name] = func
            return func
        return decorator

    def get_tool(self, name: str) -> Callable[..., Any]:
        """Retrieve the registered tool function by name."""
        if name not in self._registry:
            raise KeyError(
                f"Tool '{name}' is not registered. Registered tools: {list(self._registry.keys())}"
            )
        return self._registry[name]

    def execute_tool(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Invoke a tool function dynamically by name."""
        tool_func = self.get_tool(name)
        return tool_func(*args, **kwargs)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._registry.keys())

# Global tool registry instance
tool_registry = ToolRegistry()

def register_tool(name: str):
    """Wrapper decorator for register_tool."""
    return tool_registry.register(name)
