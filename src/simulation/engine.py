"""
Circuit Simulation Engine
Simulates electrical behavior of components
"""

import numpy as np
from typing import Dict, List, Optional
from ..models.circuit import Circuit
from ..models.component import Component, Pin


class SimulationEngine:
    """Circuit simulation engine using modified nodal analysis"""
    
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.time = 0.0
        self.node_voltages: Dict[str, float] = {}
        self.component_currents: Dict[str, Dict[str, float]] = {}
        
    def reset(self):
        """Reset simulation state"""
        self.time = 0.0
        self.node_voltages.clear()
        self.component_currents.clear()
        
    def step(self, dt: float):
        """Perform one simulation time step"""
        self.time += dt
        
        # Build circuit equations
        self.build_node_map()
        self.solve_dc_circuit()
        self.update_component_states()
        
    def build_node_map(self):
        """Build map of electrical nodes from connections"""
        # Each connection creates a node
        # Connected pins share the same node
        self.nodes: Dict[str, List[tuple]] = {}  # node_id -> [(comp_id, pin_name), ...]
        node_counter = 0
        
        # Ground node (reference)
        self.nodes['gnd'] = []
        
        # Track which pins have been assigned nodes
        pin_to_node: Dict[tuple, str] = {}
        
        for connection in self.circuit.connections:
            from_pin_key = (connection.from_component, connection.from_pin)
            to_pin_key = (connection.to_component, connection.to_pin)
            
            # Check if either pin already has a node
            from_node = pin_to_node.get(from_pin_key)
            to_node = pin_to_node.get(to_pin_key)
            
            if from_node and to_node:
                # Both pins have nodes - merge them
                if from_node != to_node:
                    self.nodes[from_node].extend(self.nodes[to_node])
                    for pin in self.nodes[to_node]:
                        pin_to_node[pin] = from_node
                    del self.nodes[to_node]
            elif from_node:
                # Only from pin has node
                self.nodes[from_node].append(to_pin_key)
                pin_to_node[to_pin_key] = from_node
            elif to_node:
                # Only to pin has node
                self.nodes[to_node].append(from_pin_key)
                pin_to_node[from_pin_key] = to_node
            else:
                # Neither has node - create new one
                node_id = f'n{node_counter}'
                node_counter += 1
                self.nodes[node_id] = [from_pin_key, to_pin_key]
                pin_to_node[from_pin_key] = node_id
                pin_to_node[to_pin_key] = node_id
                
        # Identify ground connections (battery negative terminals)
        for component in self.circuit.components.values():
            if component.type == 'battery':
                neg_pin_key = (component.id, 'negative')
                if neg_pin_key in pin_to_node:
                    # Set this node as ground
                    node_id = pin_to_node[neg_pin_key]
                    self.nodes['gnd'].extend(self.nodes[node_id])
                    for pin in self.nodes[node_id]:
                        pin_to_node[pin] = 'gnd'
                    if node_id != 'gnd':
                        del self.nodes[node_id]
                        
        self.pin_to_node = pin_to_node
        
    def solve_dc_circuit(self):
        """Solve DC circuit using nodal analysis"""
        # Simplified DC analysis for basic circuits
        
        # Initialize all nodes to 0V (except sources)
        for node_id in self.nodes:
            self.node_voltages[node_id] = 0.0
            
        # Set voltage source nodes
        for component in self.circuit.components.values():
            if component.type == 'battery':
                voltage = component.properties.get('voltage', 5.0)
                pos_pin_key = (component.id, 'positive')
                if pos_pin_key in self.pin_to_node:
                    pos_node = self.pin_to_node[pos_pin_key]
                    self.node_voltages[pos_node] = voltage
                    
        # Iterative solver for resistive circuits
        # (Simplified - for complex circuits, use matrix solver)
        max_iterations = 100
        tolerance = 0.001
        
        for iteration in range(max_iterations):
            old_voltages = self.node_voltages.copy()
            
            # Update node voltages based on connected components
            for node_id, pins in self.nodes.items():
                if node_id == 'gnd':
                    continue
                    
                # Check if this node is directly connected to a voltage source
                is_source_node = False
                for comp_id, pin_name in pins:
                    component = self.circuit.get_component(comp_id)
                    if component and component.type == 'battery' and pin_name == 'positive':
                        is_source_node = True
                        break
                        
                if is_source_node:
                    continue  # Voltage is fixed
                    
                # For other nodes, calculate based on neighboring nodes and resistances
                # This is a simplified approach
                self.update_node_voltage(node_id)
                
            # Check convergence
            max_change = max(abs(self.node_voltages[n] - old_voltages.get(n, 0)) 
                           for n in self.node_voltages)
            if max_change < tolerance:
                break
                
    def update_node_voltage(self, node_id: str):
        """Update voltage at a node based on connected components"""
        # Simplified voltage calculation
        # In a real implementation, this would use KCL and component models
        pass
        
    def update_component_states(self):
        """Update component pin voltages and currents"""
        for component in self.circuit.components.values():
            self.update_component(component)
            
    def update_component(self, component: Component):
        """Update individual component state"""
        if component.type == 'battery':
            self.update_battery(component)
        elif component.type == 'resistor':
            self.update_resistor(component)
        elif component.type == 'led':
            self.update_led(component)
            
    def update_battery(self, component: Component):
        """Update battery component"""
        voltage = component.properties.get('voltage', 5.0)
        
        # Set pin voltages
        pos_pin = component.get_pin('positive')
        neg_pin = component.get_pin('negative')
        
        if pos_pin:
            pos_pin.voltage = voltage
            # Calculate current based on load
            pos_pin.current = self.calculate_output_current(component, 'positive')
            
        if neg_pin:
            neg_pin.voltage = 0.0
            neg_pin.current = -pos_pin.current if pos_pin else 0.0
            
    def update_resistor(self, component: Component):
        """Update resistor component"""
        resistance = component.properties.get('resistance', 1000.0)
        
        pin1 = component.get_pin('pin1')
        pin2 = component.get_pin('pin2')
        
        if pin1 and pin2:
            # Get node voltages
            pin1_key = (component.id, 'pin1')
            pin2_key = (component.id, 'pin2')
            
            v1 = self.node_voltages.get(self.pin_to_node.get(pin1_key, 'gnd'), 0.0)
            v2 = self.node_voltages.get(self.pin_to_node.get(pin2_key, 'gnd'), 0.0)
            
            pin1.voltage = v1
            pin2.voltage = v2
            
            # Ohm's law: I = V/R
            current = (v1 - v2) / resistance if resistance > 0 else 0.0
            pin1.current = current
            pin2.current = -current
            
    def update_led(self, component: Component):
        """Update LED component"""
        forward_voltage = component.properties.get('forward_voltage', 2.0)
        max_current = component.properties.get('max_current', 0.020)
        
        anode = component.get_pin('anode')
        cathode = component.get_pin('cathode')
        
        if anode and cathode:
            # Get node voltages
            anode_key = (component.id, 'anode')
            cathode_key = (component.id, 'cathode')
            
            v_anode = self.node_voltages.get(self.pin_to_node.get(anode_key, 'gnd'), 0.0)
            v_cathode = self.node_voltages.get(self.pin_to_node.get(cathode_key, 'gnd'), 0.0)
            
            anode.voltage = v_anode
            cathode.voltage = v_cathode
            
            # LED model: conducts if forward biased
            voltage_drop = v_anode - v_cathode
            
            if voltage_drop > forward_voltage:
                # Simple model: LED conducts with forward voltage drop
                # Current limited by series resistance in circuit
                current = self.calculate_led_current(component, voltage_drop, forward_voltage)
                current = min(current, max_current)
            else:
                current = 0.0
                
            anode.current = current
            cathode.current = -current
            
    def calculate_output_current(self, component: Component, pin_name: str) -> float:
        """Calculate current output from a source pin"""
        # Sum currents through all loads
        total_current = 0.0
        
        # Find all components connected to this pin
        pin_key = (component.id, pin_name)
        if pin_key not in self.pin_to_node:
            return 0.0
            
        node_id = self.pin_to_node[pin_key]
        
        # Calculate total conductance and current
        for comp in self.circuit.components.values():
            if comp.type == 'resistor':
                # Check if resistor is connected to this node
                if self.is_component_on_node(comp, node_id):
                    resistance = comp.properties.get('resistance', 1000.0)
                    voltage = component.properties.get('voltage', 5.0)
                    total_current += voltage / resistance
                    
        return total_current
        
    def calculate_led_current(self, led: Component, v_drop: float, v_forward: float) -> float:
        """Calculate LED current based on series resistance"""
        # Find series resistor
        for connection in self.circuit.connections:
            if connection.to_component == led.id or connection.from_component == led.id:
                # Check if connected component is a resistor
                other_id = (connection.from_component if connection.to_component == led.id 
                           else connection.to_component)
                other = self.circuit.get_component(other_id)
                
                if other and other.type == 'resistor':
                    resistance = other.properties.get('resistance', 220.0)
                    # I = (V_supply - V_led) / R
                    current = max(0, (v_drop - v_forward) / resistance)
                    return current
                    
        # No series resistor found - limit current
        return 0.001  # 1mA default
        
    def is_component_on_node(self, component: Component, node_id: str) -> bool:
        """Check if component is connected to a node"""
        for pin in component.pins:
            pin_key = (component.id, pin.name)
            if pin_key in self.pin_to_node:
                if self.pin_to_node[pin_key] == node_id:
                    return True
        return False
