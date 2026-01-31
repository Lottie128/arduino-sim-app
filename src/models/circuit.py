"""
Circuit data model
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .component import Component, Connection


@dataclass
class Circuit:
    """Complete circuit representation"""
    components: Dict[str, Component] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)
    name: str = "Untitled Circuit"
    
    def add_component(self, component: Component):
        """Add component to circuit"""
        self.components[component.id] = component
        
    def remove_component(self, component_id: str):
        """Remove component from circuit"""
        if component_id in self.components:
            # Remove all connections involving this component
            self.connections = [
                conn for conn in self.connections
                if conn.from_component != component_id and conn.to_component != component_id
            ]
            del self.components[component_id]
            
    def get_component(self, component_id: str) -> Optional[Component]:
        """Get component by ID"""
        return self.components.get(component_id)
        
    def add_connection(self, connection: Connection):
        """Add connection between components"""
        self.connections.append(connection)
        
    def remove_connection(self, connection_id: str):
        """Remove connection"""
        self.connections = [
            conn for conn in self.connections
            if conn.id != connection_id
        ]
        
    def get_connections_for_component(self, component_id: str) -> List[Connection]:
        """Get all connections for a component"""
        return [
            conn for conn in self.connections
            if conn.from_component == component_id or conn.to_component == component_id
        ]
        
    def validate(self) -> List[str]:
        """Validate circuit and return list of errors"""
        errors = []
        
        # Check for floating components (no connections)
        for comp_id, component in self.components.items():
            conns = self.get_connections_for_component(comp_id)
            if not conns and component.type not in ['battery']:
                errors.append(f"Component {component.name} has no connections")
                
        # Check for short circuits (direct battery terminal connections)
        for component in self.components.values():
            if component.type == 'battery':
                # Check if positive and negative are directly connected
                pos_connections = [c for c in self.connections 
                                 if (c.from_component == component.id and c.from_pin == 'positive') or
                                    (c.to_component == component.id and c.to_pin == 'positive')]
                neg_connections = [c for c in self.connections
                                 if (c.from_component == component.id and c.from_pin == 'negative') or
                                    (c.to_component == component.id and c.to_pin == 'negative')]
                                    
                # Check for direct connections without load
                for pos_conn in pos_connections:
                    for neg_conn in neg_connections:
                        if (pos_conn.to_component == neg_conn.from_component or 
                            pos_conn.from_component == neg_conn.to_component):
                            load_comp = self.get_component(
                                pos_conn.to_component if pos_conn.to_component != component.id 
                                else pos_conn.from_component
                            )
                            if load_comp and load_comp.type == 'battery':
                                errors.append("Short circuit detected: Battery terminals directly connected")
                                
        return errors
