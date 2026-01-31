# Wiring Guide - How to Trace Connections

## Creating Connections

### Method 1: Right-Click Wiring (Interactive)

1. **Right-click on a component pin** (the small circles on components)
2. A **dashed blue line** appears following your mouse
3. **Right-click on another pin** to complete the connection
4. A **green wire** appears connecting the two pins

### Method 2: Component Panel (Drag & Drop)

1. Double-click a component in the left panel
2. Component appears at canvas center
3. Drag component to desired position
4. Right-click pins to wire as above

## Visual Feedback

### Pin States
- **Gray** - No voltage (0V)
- **Yellow** - Intermediate voltage (0.5V - 4.5V)
- **Red** - High voltage (>4.5V)
- **Blue highlight** - Pin is hovered (ready to connect)
- **Scale up 1.3x** - Pin is ready for connection

### Wire States
- **Green (dim)** - No current flowing
- **Green (bright)** - Current flowing (brightness = current intensity)
- **Dashed blue** - Temporary wire during connection
- **Thickness** - 3px for normal wires

### Component States
- **LED**:
  - Dark/dim - No current
  - Glowing - Current flowing (brightness proportional to current)
  - Radial gradient - Realistic glow effect
- **Battery**:
  - Red terminal - Positive (+)
  - Blue terminal - Negative (-)
  - White text - Voltage label
- **Resistor**:
  - Brown bands - Resistance value indicator
  - Text label - Actual resistance in Ohms

## Debugging Connections

### Console Output

When you create connections, check the terminal for:
```
Connected: Battery(positive) -> Resistor(pin1)
Connected: Resistor(pin2) -> LED(anode)
Connected: LED(cathode) -> Battery(negative)
```

### Circuit Validation

The app validates:
- Floating components (no connections)
- Short circuits (direct battery terminal connections)
- Missing ground paths

### Trace Connection Path

Press **Ctrl+D** or use **Debug > Show Connections** to see:
- All connections listed
- Component IDs
- Pin names
- Connection IDs

## Connection Tracing in Code

### Print All Connections

```python
# In examples/battery_led.py or your own script
for conn in canvas.circuit.connections:
    print(f"Connection {conn.id}:")
    print(f"  From: {conn.from_component} pin {conn.from_pin}")
    print(f"  To: {conn.to_component} pin {conn.to_pin}")
```

### Trace Specific Component

```python
# Find all connections for a component
component_id = "abc-123-def"
connections = canvas.circuit.get_connections_for_component(component_id)
for conn in connections:
    print(f"  Connected to: {conn.to_component}")
```

### Get Node Information

```python
# Show electrical nodes (connected pins)
canvas.simulation_engine.build_node_map()
for node_id, pins in canvas.simulation_engine.nodes.items():
    print(f"Node {node_id}:")
    for comp_id, pin_name in pins:
        comp = canvas.circuit.get_component(comp_id)
        print(f"  - {comp.name} ({comp.type}) pin {pin_name}")
```

## Keyboard Shortcuts

- **Right-click pin** - Start/complete wiring
- **ESC** - Cancel wiring
- **Delete** - Remove selected component
- **Ctrl+Z** - Undo (future feature)
- **Ctrl+D** - Debug: Show all connections
- **F5** - Start simulation
- **Shift+F5** - Stop simulation

## Common Connection Patterns

### Simple LED Circuit
```
Battery(+) -> Resistor -> LED(anode)
LED(cathode) -> Battery(-)
```

### Parallel LEDs
```
Battery(+) -> Resistor1 -> LED1(anode)
          \-> Resistor2 -> LED2(anode)
LED1(cathode) -> Battery(-)
LED2(cathode) -> Battery(-)
```

### Series Circuit
```
Battery(+) -> Resistor1 -> Resistor2 -> LED(anode)
LED(cathode) -> Battery(-)
```

## Troubleshooting

### Wire Not Appearing
- Make sure you right-click (not left-click) on pins
- Both pins must be on different components
- Check console for error messages

### LED Not Lighting
- Check if simulation is running (F5)
- Verify complete circuit path
- Check resistor value (too high = no current)
- Verify LED orientation (anode to +, cathode to -)

### Can't Select Pin
- Zoom in closer (mouse wheel)
- Pins are 10px diameter circles
- Hover over pin - it should turn blue and scale up

### Connection Disappeared
- Wires are behind components (z-index issue)
- Check console - connection might have failed validation
- Try recreating the connection

## Tips

1. **Start with power** - Place battery first
2. **Add load** - LED or resistor
3. **Complete circuit** - Must return to battery negative
4. **Test incrementally** - Add one connection, test, then continue
5. **Use simulation** - F5 to see if current flows
6. **Watch colors** - Pins and wires change color with voltage/current
