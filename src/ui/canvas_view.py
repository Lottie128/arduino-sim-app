# Add to existing canvas_view.py - connection tracing helpers
# This shows the additions needed for better connection visualization

# ... existing imports ...

def add_connection_tracing_to_canvas():
    """
    Add these methods to the CanvasView class for connection tracing
    """
    pass

# Add this method to CanvasView class:
def show_connection_trace(self):
    """Show all connections in a debug window"""
    print("\n" + "="*60)
    print("CONNECTION TRACE")
    print("="*60)
    
    if not self.circuit.connections:
        print("No connections found")
        return
    
    for i, conn in enumerate(self.circuit.connections, 1):
        from_comp = self.circuit.get_component(conn.from_component)
        to_comp = self.circuit.get_component(conn.to_component)
        
        print(f"\n{i}. Connection ID: {conn.id}")
        if from_comp:
            print(f"   FROM: {from_comp.name} ({from_comp.type})")
            print(f"         Pin: {conn.from_pin}")
            from_pin = from_comp.get_pin(conn.from_pin)
            if from_pin:
                print(f"         Voltage: {from_pin.voltage:.2f}V")
                print(f"         Current: {from_pin.current*1000:.2f}mA")
        
        if to_comp:
            print(f"   TO:   {to_comp.name} ({to_comp.type})")
            print(f"         Pin: {conn.to_pin}")
            to_pin = to_comp.get_pin(conn.to_pin)
            if to_pin:
                print(f"         Voltage: {to_pin.voltage:.2f}V")
                print(f"         Current: {to_pin.current*1000:.2f}mA")
    
    print("\n" + "="*60)
    
    # Show node map
    print("\nELECTRICAL NODES")
    print("="*60)
    self.simulation_engine.build_node_map()
    for node_id, pins in self.simulation_engine.nodes.items():
        voltage = self.simulation_engine.node_voltages.get(node_id, 0.0)
        print(f"\nNode '{node_id}': {voltage:.2f}V")
        for comp_id, pin_name in pins:
            comp = self.circuit.get_component(comp_id)
            if comp:
                print(f"  - {comp.name} ({comp.type}) pin '{pin_name}'")
    print("\n" + "="*60)

# Add this method to CanvasView class:
def highlight_connection(self, connection_id: str):
    """Highlight a specific connection"""
    for wire_item in self.wire_items:
        if wire_item.connection.id == connection_id:
            # Highlight the wire
            from .qt_compat import QPen, QColor
            wire_item.setPen(QPen(QColor(255, 255, 0), 5))  # Yellow, thick
            wire_item.setZValue(100)  # Bring to front
            
            # Flash effect
            from .qt_compat import QTimer
            def reset_wire():
                wire_item.setPen(QPen(QColor(50, 150, 50), 3))
                wire_item.setZValue(1)
            QTimer.singleShot(2000, reset_wire)  # Reset after 2 seconds
            break

# Add this method to CanvasView class:
def keyPressEvent(self, event):
    """Handle keyboard shortcuts"""
    from .qt_compat import Qt
    
    try:
        # PyQt6
        if event.key() == Qt.Key.Key_D and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.show_connection_trace()
        elif event.key() == Qt.Key.Key_Escape:
            if self.wiring_mode:
                self.cancel_wiring()
        elif event.key() == Qt.Key.Key_Delete:
            # Delete selected items
            for item in self.scene.selectedItems():
                if isinstance(item, ComponentGraphicsItem):
                    self.remove_component(item.component.id)
    except:
        # PyQt5
        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.show_connection_trace()
        elif event.key() == Qt.Key_Escape:
            if self.wiring_mode:
                self.cancel_wiring()
        elif event.key() == Qt.Key_Delete:
            for item in self.scene.selectedItems():
                if isinstance(item, ComponentGraphicsItem):
                    self.remove_component(item.component.id)
    
    super().keyPressEvent(event)

# Add this method to CanvasView class:
def remove_component(self, component_id: str):
    """Remove a component and its connections"""
    if component_id in self.component_items:
        # Remove graphics item
        graphics_item = self.component_items[component_id]
        self.scene.removeItem(graphics_item)
        del self.component_items[component_id]
        
        # Remove from circuit (this also removes connections)
        self.circuit.remove_component(component_id)
        
        # Remove wire graphics items
        self.wire_items = [
            wire for wire in self.wire_items
            if wire.connection.from_component != component_id 
            and wire.connection.to_component != component_id
        ]
        
        self.component_removed.emit(component_id)
        print(f"Removed component: {component_id}")
