"""
Component data models
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import uuid


@dataclass
class Pin:
    """Component pin/terminal"""
    name: str
    type: str  # 'input', 'output', 'passive', 'power', 'ground'
    position: Tuple[float, float]  # Relative position (x, y)
    voltage: float = 0.0
    current: float = 0.0
    connected_to: List[str] = field(default_factory=list)  # List of connection IDs


@dataclass
class Component:
    """Base component class"""
    type: str
    name: str
    pins: List[Pin]
    properties: Dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def get_pin(self, pin_name: str) -> Optional[Pin]:
        """Get pin by name"""
        for pin in self.pins:
            if pin.name == pin_name:
                return pin
        return None
        
    def set_property(self, key: str, value):
        """Set component property"""
        self.properties[key] = value
        
    def get_property(self, key: str, default=None):
        """Get component property"""
        return self.properties.get(key, default)


@dataclass
class Connection:
    """Connection between component pins"""
    from_component: str
    from_pin: str
    to_component: str
    to_pin: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resistance: float = 0.001  # Wire resistance in ohms
