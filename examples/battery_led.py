#!/usr/bin/env python3
"""
Example: Simple Battery and LED Circuit
Demonstrates basic circuit creation, connection, and simulation
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ui.qt_compat import QApplication, QPointF, QTimer, exec_app
from src.ui.canvas_view import CanvasView, WireGraphicsItem
from src.models.component import Connection


def create_battery_led_circuit(canvas: CanvasView):
    """
    Creates a simple circuit:
    Battery (5V) -> Resistor (220Ω) -> LED -> back to Battery
    """
    
    print("Creating Battery + LED Circuit...")
    
    # Add components to canvas
    canvas.add_component('battery', QPointF(-200, 0))
    canvas.add_component('resistor', QPointF(0, -100))
    canvas.add_component('led', QPointF(200, 0))
    
    # Get component references
    components = list(canvas.circuit.components.values())
    battery = next(c for c in components if c.type == 'battery')
    resistor = next(c for c in components if c.type == 'resistor')
    led = next(c for c in components if c.type == 'led')
    
    print(f"Battery ID: {battery.id}")
    print(f"Resistor ID: {resistor.id}")
    print(f"LED ID: {led.id}")
    
    # Create connections
    connection1 = Connection(
        from_component=battery.id,
        from_pin='positive',
        to_component=resistor.id,
        to_pin='pin1'
    )
    canvas.circuit.add_connection(connection1)
    print(f"Connected: Battery(+) -> Resistor(pin1)")
    
    connection2 = Connection(
        from_component=resistor.id,
        from_pin='pin2',
        to_component=led.id,
        to_pin='anode'
    )
    canvas.circuit.add_connection(connection2)
    print(f"Connected: Resistor(pin2) -> LED(anode)")
    
    connection3 = Connection(
        from_component=led.id,
        from_pin='cathode',
        to_component=battery.id,
        to_pin='negative'
    )
    canvas.circuit.add_connection(connection3)
    print(f"Connected: LED(cathode) -> Battery(-)")
    
    # Create wire graphics items
    battery_item = canvas.component_items[battery.id]
    resistor_item = canvas.component_items[resistor.id]
    led_item = canvas.component_items[led.id]
    
    # Wire 1: Battery to Resistor
    start_pos1 = battery_item.mapToScene(battery_item.pin_items['positive'].pos())
    end_pos1 = resistor_item.mapToScene(resistor_item.pin_items['pin1'].pos())
    wire1 = WireGraphicsItem(connection1, start_pos1, end_pos1)
    canvas.scene.addItem(wire1)
    canvas.wire_items.append(wire1)
    
    # Wire 2: Resistor to LED
    start_pos2 = resistor_item.mapToScene(resistor_item.pin_items['pin2'].pos())
    end_pos2 = led_item.mapToScene(led_item.pin_items['anode'].pos())
    wire2 = WireGraphicsItem(connection2, start_pos2, end_pos2)
    canvas.scene.addItem(wire2)
    canvas.wire_items.append(wire2)
    
    # Wire 3: LED to Battery
    start_pos3 = led_item.mapToScene(led_item.pin_items['cathode'].pos())
    end_pos3 = battery_item.mapToScene(battery_item.pin_items['negative'].pos())
    wire3 = WireGraphicsItem(connection3, start_pos3, end_pos3)
    canvas.scene.addItem(wire3)
    canvas.wire_items.append(wire3)
    
    print("\nCircuit created successfully!")
    print(f"Components: {len(canvas.circuit.components)}")
    print(f"Connections: {len(canvas.circuit.connections)}")
    
    # Print expected behavior
    print("\n" + "="*60)
    print("EXPECTED BEHAVIOR:")
    print("="*60)
    print(f"Battery voltage: {battery.properties['voltage']}V")
    print(f"Resistor: {resistor.properties['resistance']}Ω")
    print(f"LED forward voltage: {led.properties['forward_voltage']}V")
    print(f"LED max current: {led.properties['max_current']*1000}mA")
    print("\nCalculated values:")
    voltage_drop = battery.properties['voltage'] - led.properties['forward_voltage']
    current = voltage_drop / resistor.properties['resistance']
    print(f"Voltage across resistor: {voltage_drop}V")
    print(f"Current through circuit: {current*1000:.2f}mA")
    print(f"\nLED should light up with brightness: {min(1.0, current/led.properties['max_current'])*100:.0f}%")
    print("="*60)


def main():
    """Run the example"""
    app = QApplication(sys.argv)
    
    # Create canvas
    canvas = CanvasView()
    canvas.resize(1000, 800)
    canvas.setWindowTitle('Example: Battery + LED Circuit')
    canvas.show()
    
    # Create the circuit
    create_battery_led_circuit(canvas)
    
    # Start simulation after 1 second
    def start_sim():
        print("\n" + "="*60)
        print("Starting simulation...")
        print("Watch the LED light up!")
        print("="*60)
        canvas.start_simulation()
    
    QTimer.singleShot(1000, start_sim)
    
    # Print instructions
    print("\n" + "="*60)
    print("INTERACTIVE CONTROLS:")
    print("="*60)
    print("- Mouse wheel: Zoom in/out")
    print("- Click and drag: Pan the canvas")
    print("- Right-click on pins: Create connections (wiring mode)")
    print("- Select components: Click to select, drag to move")
    print("="*60)
    
    sys.exit(exec_app(app))


if __name__ == '__main__':
    main()
