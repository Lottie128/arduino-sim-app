#!/usr/bin/env python3
"""
Connection Tracing Example
Demonstrates how to trace and debug circuit connections
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ui.qt_compat import QApplication, QPointF, QTimer, exec_app
from src.ui.canvas_view import CanvasView, WireGraphicsItem
from src.models.component import Connection


def create_test_circuit(canvas: CanvasView):
    """
    Create a test circuit with multiple connections
    """
    print("\n" + "="*60)
    print("CREATING TEST CIRCUIT")
    print("="*60)
    
    # Add components
    canvas.add_component('battery', QPointF(-200, 0))
    canvas.add_component('resistor', QPointF(0, 0))
    canvas.add_component('led', QPointF(200, 0))
    
    components = list(canvas.circuit.components.values())
    battery = next(c for c in components if c.type == 'battery')
    resistor = next(c for c in components if c.type == 'resistor')
    led = next(c for c in components if c.type == 'led')
    
    print(f"\nAdded components:")
    print(f"  1. Battery: ID={battery.id[:8]}...")
    print(f"  2. Resistor: ID={resistor.id[:8]}...")
    print(f"  3. LED: ID={led.id[:8]}...")
    
    # Create connections
    print(f"\nCreating connections...")
    
    connection1 = Connection(
        from_component=battery.id,
        from_pin='positive',
        to_component=resistor.id,
        to_pin='pin1'
    )
    canvas.circuit.add_connection(connection1)
    print(f"  ✓ Battery(+) -> Resistor(pin1) [ID: {connection1.id[:8]}...]")
    
    connection2 = Connection(
        from_component=resistor.id,
        from_pin='pin2',
        to_component=led.id,
        to_pin='anode'
    )
    canvas.circuit.add_connection(connection2)
    print(f"  ✓ Resistor(pin2) -> LED(anode) [ID: {connection2.id[:8]}...]")
    
    connection3 = Connection(
        from_component=led.id,
        from_pin='cathode',
        to_component=battery.id,
        to_pin='negative'
    )
    canvas.circuit.add_connection(connection3)
    print(f"  ✓ LED(cathode) -> Battery(-) [ID: {connection3.id[:8]}...]")
    
    # Create wire graphics
    battery_item = canvas.component_items[battery.id]
    resistor_item = canvas.component_items[resistor.id]
    led_item = canvas.component_items[led.id]
    
    # Wire 1
    start_pos1 = battery_item.mapToScene(battery_item.pin_items['positive'].pos())
    end_pos1 = resistor_item.mapToScene(resistor_item.pin_items['pin1'].pos())
    wire1 = WireGraphicsItem(connection1, start_pos1, end_pos1)
    canvas.scene.addItem(wire1)
    canvas.wire_items.append(wire1)
    
    # Wire 2
    start_pos2 = resistor_item.mapToScene(resistor_item.pin_items['pin2'].pos())
    end_pos2 = led_item.mapToScene(led_item.pin_items['anode'].pos())
    wire2 = WireGraphicsItem(connection2, start_pos2, end_pos2)
    canvas.scene.addItem(wire2)
    canvas.wire_items.append(wire2)
    
    # Wire 3
    start_pos3 = led_item.mapToScene(led_item.pin_items['cathode'].pos())
    end_pos3 = battery_item.mapToScene(battery_item.pin_items['negative'].pos())
    wire3 = WireGraphicsItem(connection3, start_pos3, end_pos3)
    canvas.scene.addItem(wire3)
    canvas.wire_items.append(wire3)
    
    print(f"\n✓ Circuit created with {len(canvas.circuit.components)} components")
    print(f"✓ Total connections: {len(canvas.circuit.connections)}")
    print("="*60)
    
    return connection1, connection2, connection3


def trace_connections(canvas: CanvasView):
    """
    Demonstrate connection tracing
    """
    print("\n" + "="*60)
    print("TRACING CONNECTIONS")
    print("="*60)
    
    # Method 1: List all connections
    print("\n1. All Connections:")
    print("-" * 40)
    for i, conn in enumerate(canvas.circuit.connections, 1):
        from_comp = canvas.circuit.get_component(conn.from_component)
        to_comp = canvas.circuit.get_component(conn.to_component)
        print(f"{i}. {from_comp.name}.{conn.from_pin} -> {to_comp.name}.{conn.to_pin}")
    
    # Method 2: Trace specific component
    print("\n2. Component Connection Map:")
    print("-" * 40)
    for comp_id, comp in canvas.circuit.components.items():
        connections = canvas.circuit.get_connections_for_component(comp_id)
        print(f"{comp.name} ({comp.type}):")
        for conn in connections:
            if conn.from_component == comp_id:
                to_comp = canvas.circuit.get_component(conn.to_component)
                print(f"  → {to_comp.name}.{conn.to_pin}")
            else:
                from_comp = canvas.circuit.get_component(conn.from_component)
                print(f"  ← {from_comp.name}.{conn.from_pin}")
    
    # Method 3: Show electrical nodes
    print("\n3. Electrical Nodes (after simulation):")
    print("-" * 40)
    print("Starting simulation to build node map...")
    canvas.start_simulation()
    QTimer.singleShot(500, lambda: show_nodes(canvas))


def show_nodes(canvas: CanvasView):
    """Show node information"""
    canvas.stop_simulation()
    
    if hasattr(canvas.simulation_engine, 'nodes'):
        for node_id, pins in canvas.simulation_engine.nodes.items():
            voltage = canvas.simulation_engine.node_voltages.get(node_id, 0.0)
            print(f"Node '{node_id}' @ {voltage:.2f}V:")
            for comp_id, pin_name in pins:
                comp = canvas.circuit.get_component(comp_id)
                if comp:
                    pin = comp.get_pin(pin_name)
                    if pin:
                        print(f"  - {comp.name}.{pin_name}: "
                              f"V={pin.voltage:.2f}V, I={pin.current*1000:.2f}mA")
    
    print("\n" + "="*60)
    print("\nKEYBOARD SHORTCUTS:")
    print("  Ctrl+D  - Show connection trace")
    print("  ESC     - Cancel wiring")
    print("  Delete  - Remove selected component")
    print("  F5      - Start simulation")
    print("="*60)


def main():
    """Run the tracing example"""
    app = QApplication(sys.argv)
    
    # Create canvas
    canvas = CanvasView()
    canvas.resize(1000, 800)
    canvas.setWindowTitle('Connection Tracing Example')
    canvas.show()
    
    # Create circuit
    connections = create_test_circuit(canvas)
    
    # Trace connections after 1 second
    QTimer.singleShot(1000, lambda: trace_connections(canvas))
    
    # Highlight first connection after 3 seconds
    def highlight_demo():
        print("\n🔦 Highlighting first connection...")
        if hasattr(canvas, 'highlight_connection'):
            canvas.highlight_connection(connections[0].id)
        else:
            print("Note: highlight_connection method not yet added to canvas")
    
    QTimer.singleShot(3000, highlight_demo)
    
    sys.exit(exec_app(app))


if __name__ == '__main__':
    main()
