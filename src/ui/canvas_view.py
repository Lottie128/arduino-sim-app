"""
Circuit Design Canvas View
Handles component placement, wiring, and visual rendering
"""

from .qt_compat import (
    QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem,
    QGraphicsTextItem, QMenu, Qt, QPointF, QRectF, QTimer,
    QPen, QBrush, QColor, QPainter, QFont,
    QLinearGradient, QRadialGradient, pyqtSignal
)
from typing import Optional, List, Dict, Tuple
import math

from ..simulation.engine import SimulationEngine
from ..models.component import Component, Pin, Connection
from ..models.circuit import Circuit


class PinGraphicsItem(QGraphicsEllipseItem):
    """Visual representation of a component pin"""
    
    def __init__(self, pin: Pin, parent=None):
        super().__init__(-5, -5, 10, 10, parent)
        self.pin = pin
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.setPen(QPen(QColor(100, 100, 100), 2))
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        
    def hoverEnterEvent(self, event):
        """Highlight pin on hover"""
        self.setBrush(QBrush(QColor(100, 200, 255)))
        self.setScale(1.3)
        
    def hoverLeaveEvent(self, event):
        """Remove highlight"""
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.setScale(1.0)
        
    def update_state(self, voltage: float, current: float):
        """Update pin visual based on electrical state"""
        if voltage > 4.5:
            self.setBrush(QBrush(QColor(255, 50, 50)))  # Red for HIGH
        elif voltage > 0.5:
            self.setBrush(QBrush(QColor(255, 200, 50)))  # Yellow for intermediate
        else:
            self.setBrush(QBrush(QColor(100, 100, 100)))  # Gray for LOW


class WireGraphicsItem(QGraphicsLineItem):
    """Visual representation of a wire connection"""
    
    def __init__(self, connection: Connection, start_pos: QPointF, end_pos: QPointF):
        super().__init__()
        self.connection = connection
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # Default wire appearance
        self.setPen(QPen(QColor(50, 150, 50), 3))
        self.setZValue(1)
        self.update_line()
        
    def update_line(self):
        """Update wire path with right-angle routing"""
        # Simple L-shaped routing
        self.setLine(
            self.start_pos.x(), self.start_pos.y(),
            self.end_pos.x(), self.end_pos.y()
        )
        
    def update_current(self, current: float):
        """Update wire color based on current flow"""
        if abs(current) > 0.001:
            # Show current flow with brighter color
            intensity = min(255, int(100 + abs(current) * 1000))
            self.setPen(QPen(QColor(50, intensity, 50), 3))
        else:
            self.setPen(QPen(QColor(50, 150, 50), 3))


class ComponentGraphicsItem(QGraphicsItem):
    """Base class for component visual representation"""
    
    def __init__(self, component: Component):
        super().__init__()
        self.component = component
        self.pin_items: Dict[str, PinGraphicsItem] = {}
        try:
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        except:
            # PyQt5 compatibility
            self.setFlag(QGraphicsItem.ItemIsMovable)
            self.setFlag(QGraphicsItem.ItemIsSelectable)
            self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setZValue(5)
        self.create_pins()
        
    def create_pins(self):
        """Create visual pin items"""
        for pin in self.component.pins:
            pin_item = PinGraphicsItem(pin, self)
            pin_item.setPos(pin.position[0], pin.position[1])
            self.pin_items[pin.name] = pin_item
            
    def boundingRect(self):
        return QRectF(-30, -30, 60, 60)
        
    def paint(self, painter, option, widget):
        # Override in subclasses
        pass
        
    def update_state(self):
        """Update visual state based on simulation"""
        for pin_name, pin_item in self.pin_items.items():
            pin = self.component.get_pin(pin_name)
            if pin:
                pin_item.update_state(pin.voltage, pin.current)


class BatteryGraphicsItem(ComponentGraphicsItem):
    """Visual representation of a battery"""
    
    def paint(self, painter, option, widget):
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        except:
            painter.setRenderHint(QPainter.Antialiasing)
        
        # Battery body
        painter.setBrush(QBrush(QColor(80, 80, 80)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(-25, -15, 50, 30)
        
        # Positive terminal
        painter.setBrush(QBrush(QColor(200, 50, 50)))
        painter.drawRect(25, -8, 8, 16)
        
        # Negative terminal
        painter.setBrush(QBrush(QColor(50, 50, 200)))
        painter.drawRect(-33, -5, 8, 10)
        
        # Voltage label
        painter.setPen(QPen(QColor(255, 255, 255)))
        try:
            painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        except:
            painter.setFont(QFont('Arial', 10, QFont.Bold))
        try:
            painter.drawText(QRectF(-25, -15, 50, 30), Qt.AlignmentFlag.AlignCenter, 
                            f"{self.component.properties.get('voltage', 5)}V")
        except:
            painter.drawText(QRectF(-25, -15, 50, 30), Qt.AlignCenter, 
                            f"{self.component.properties.get('voltage', 5)}V")
        
        # Selection highlight
        if self.isSelected():
            try:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
            except:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
            painter.drawRect(-30, -20, 60, 40)


class LEDGraphicsItem(ComponentGraphicsItem):
    """Visual representation of an LED"""
    
    def __init__(self, component: Component):
        super().__init__(component)
        self.is_lit = False
        self.brightness = 0.0
        
    def paint(self, painter, option, widget):
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        except:
            painter.setRenderHint(QPainter.Antialiasing)
        
        # LED body (circle)
        color = QColor(self.component.properties.get('color', 'red'))
        
        if self.is_lit:
            # Create glow effect when lit
            gradient = QRadialGradient(0, 0, 20)
            glow_color = QColor(color)
            glow_color.setAlpha(int(200 * self.brightness))
            gradient.setColorAt(0, glow_color)
            gradient.setColorAt(0.7, color)
            gradient.setColorAt(1, color.darker(150))
            painter.setBrush(QBrush(gradient))
        else:
            # Dim when off
            painter.setBrush(QBrush(color.darker(300)))
            
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(-15, -15, 30, 30)
        
        # LED leads (anode and cathode)
        painter.setPen(QPen(QColor(150, 150, 150), 3))
        painter.drawLine(0, 15, 0, 25)  # Anode (bottom)
        painter.drawLine(0, -15, 0, -25)  # Cathode (top)
        
        # Cathode flat indicator
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawLine(-10, -15, 10, -15)
        
        # Selection highlight
        if self.isSelected():
            try:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
            except:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
            painter.drawRect(-20, -30, 40, 60)
            
    def update_state(self):
        """Update LED brightness based on current"""
        super().update_state()
        
        # Get current through LED
        anode_pin = self.component.get_pin('anode')
        if anode_pin and anode_pin.current > 0.001:  # 1mA threshold
            self.is_lit = True
            # Brightness proportional to current (max at 20mA)
            self.brightness = min(1.0, anode_pin.current / 0.020)
        else:
            self.is_lit = False
            self.brightness = 0.0
        
        self.update()


class ResistorGraphicsItem(ComponentGraphicsItem):
    """Visual representation of a resistor"""
    
    def paint(self, painter, option, widget):
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        except:
            painter.setRenderHint(QPainter.Antialiasing)
        
        # Resistor body
        painter.setBrush(QBrush(QColor(210, 180, 140)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(-20, -8, 40, 16)
        
        # Color bands for resistance value
        painter.setPen(QPen(QColor(139, 69, 19), 3))
        painter.drawLine(-12, -8, -12, 8)
        painter.drawLine(-4, -8, -4, 8)
        painter.drawLine(4, -8, 4, 8)
        
        # Leads
        painter.setPen(QPen(QColor(150, 150, 150), 3))
        painter.drawLine(-20, 0, -30, 0)
        painter.drawLine(20, 0, 30, 0)
        
        # Value label
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont('Arial', 8))
        try:
            painter.drawText(QRectF(-20, 10, 40, 20), Qt.AlignmentFlag.AlignCenter,
                            f"{self.component.properties.get('resistance', 220)}Ω")
        except:
            painter.drawText(QRectF(-20, 10, 40, 20), Qt.AlignCenter,
                            f"{self.component.properties.get('resistance', 220)}Ω")
        
        if self.isSelected():
            try:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
            except:
                painter.setPen(QPen(QColor(100, 200, 255), 2, Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
            painter.drawRect(-35, -15, 70, 45)


class CanvasView(QGraphicsView):
    """Main canvas for circuit design"""
    
    component_added = pyqtSignal(str)
    component_removed = pyqtSignal(str)
    connection_created = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Canvas settings
        try:
            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        except:
            self.setRenderHint(QPainter.Antialiasing)
            self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        
        # Circuit model
        self.circuit = Circuit()
        self.simulation_engine = SimulationEngine(self.circuit)
        
        # Visual tracking
        self.component_items: Dict[str, ComponentGraphicsItem] = {}
        self.wire_items: List[WireGraphicsItem] = []
        
        # Wiring state
        self.wiring_mode = False
        self.wiring_start_pin: Optional[Tuple[str, str]] = None
        self.temp_wire: Optional[QGraphicsLineItem] = None
        
        # Simulation timer
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.update_simulation)
        self.simulation_running = False
        
        # Setup canvas appearance
        self.setup_canvas()
        
    def setup_canvas(self):
        """Setup canvas grid and background"""
        self.setBackgroundBrush(QBrush(QColor(245, 245, 245)))
        
        # Draw grid
        grid_pen = QPen(QColor(220, 220, 220), 1)
        for x in range(-1000, 1001, 20):
            line = self.scene.addLine(x, -1000, x, 1000, grid_pen)
            line.setZValue(-10)
        for y in range(-1000, 1001, 20):
            line = self.scene.addLine(-1000, y, 1000, y, grid_pen)
            line.setZValue(-10)
    
    def add_component(self, component_type: str, position: QPointF = None):
        """Add component to canvas"""
        if position is None:
            position = QPointF(0, 0)
            
        # Create component model
        component = self.create_component(component_type)
        if not component:
            return
            
        # Add to circuit
        self.circuit.add_component(component)
        
        # Create visual representation
        graphics_item = self.create_graphics_item(component)
        graphics_item.setPos(position)
        self.scene.addItem(graphics_item)
        self.component_items[component.id] = graphics_item
        
        self.component_added.emit(component.id)
        
    def create_component(self, component_type: str) -> Optional[Component]:
        """Factory method for creating components"""
        if component_type == 'battery':
            return Component(
                type='battery',
                name='Battery',
                pins=[
                    Pin('positive', 'output', (-33, 0)),
                    Pin('negative', 'output', (33, 0))
                ],
                properties={'voltage': 5.0}
            )
        elif component_type == 'led':
            return Component(
                type='led',
                name='LED',
                pins=[
                    Pin('anode', 'input', (0, 25)),
                    Pin('cathode', 'input', (0, -25))
                ],
                properties={'color': 'red', 'forward_voltage': 2.0, 'max_current': 0.020}
            )
        elif component_type == 'resistor':
            return Component(
                type='resistor',
                name='Resistor',
                pins=[
                    Pin('pin1', 'passive', (-30, 0)),
                    Pin('pin2', 'passive', (30, 0))
                ],
                properties={'resistance': 220.0}
            )
        return None
        
    def create_graphics_item(self, component: Component) -> ComponentGraphicsItem:
        """Factory method for creating graphics items"""
        if component.type == 'battery':
            return BatteryGraphicsItem(component)
        elif component.type == 'led':
            return LEDGraphicsItem(component)
        elif component.type == 'resistor':
            return ResistorGraphicsItem(component)
        return ComponentGraphicsItem(component)
        
    def mousePressEvent(self, event):
        """Handle mouse press for wiring"""
        try:
            right_button = Qt.MouseButton.RightButton
        except:
            right_button = Qt.RightButton
            
        if event.button() == right_button:
            # Check if clicked on a pin
            item = self.itemAt(event.pos())
            if isinstance(item, PinGraphicsItem):
                self.start_wiring(item)
                return
        
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Handle mouse move for temporary wire display"""
        if self.wiring_mode and self.temp_wire:
            scene_pos = self.mapToScene(event.pos())
            line = self.temp_wire.line()
            self.temp_wire.setLine(line.x1(), line.y1(), scene_pos.x(), scene_pos.y())
        
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release to complete wiring"""
        if self.wiring_mode:
            item = self.itemAt(event.pos())
            if isinstance(item, PinGraphicsItem):
                self.complete_wiring(item)
            else:
                self.cancel_wiring()
            return
            
        super().mouseReleaseEvent(event)
        
    def start_wiring(self, pin_item: PinGraphicsItem):
        """Start wiring from a pin"""
        self.wiring_mode = True
        
        # Find component containing this pin
        component_item = pin_item.parentItem()
        if isinstance(component_item, ComponentGraphicsItem):
            self.wiring_start_pin = (component_item.component.id, pin_item.pin.name)
            
            # Create temporary wire for visual feedback
            start_pos = component_item.mapToScene(pin_item.pos())
            self.temp_wire = QGraphicsLineItem(start_pos.x(), start_pos.y(), 
                                               start_pos.x(), start_pos.y())
            try:
                self.temp_wire.setPen(QPen(QColor(100, 100, 255), 2, Qt.PenStyle.DashLine))
            except:
                self.temp_wire.setPen(QPen(QColor(100, 100, 255), 2, Qt.DashLine))
            self.scene.addItem(self.temp_wire)
            
    def complete_wiring(self, end_pin_item: PinGraphicsItem):
        """Complete wiring connection"""
        if not self.wiring_start_pin:
            self.cancel_wiring()
            return
            
        # Find end component
        end_component_item = end_pin_item.parentItem()
        if not isinstance(end_component_item, ComponentGraphicsItem):
            self.cancel_wiring()
            return
            
        start_comp_id, start_pin_name = self.wiring_start_pin
        end_comp_id = end_component_item.component.id
        end_pin_name = end_pin_item.pin.name
        
        # Don't connect pin to itself
        if start_comp_id == end_comp_id and start_pin_name == end_pin_name:
            self.cancel_wiring()
            return
            
        # Create connection in circuit model
        connection = Connection(
            from_component=start_comp_id,
            from_pin=start_pin_name,
            to_component=end_comp_id,
            to_pin=end_pin_name
        )
        self.circuit.add_connection(connection)
        
        # Create visual wire
        start_item = self.component_items[start_comp_id]
        start_pos = start_item.mapToScene(start_item.pin_items[start_pin_name].pos())
        end_pos = end_component_item.mapToScene(end_pin_item.pos())
        
        wire_item = WireGraphicsItem(connection, start_pos, end_pos)
        self.scene.addItem(wire_item)
        self.wire_items.append(wire_item)
        
        self.cancel_wiring()
        self.connection_created.emit(start_comp_id, end_comp_id)
        
    def cancel_wiring(self):
        """Cancel wiring operation"""
        self.wiring_mode = False
        self.wiring_start_pin = None
        if self.temp_wire:
            self.scene.removeItem(self.temp_wire)
            self.temp_wire = None
            
    def start_simulation(self):
        """Start circuit simulation"""
        if not self.simulation_running:
            self.simulation_running = True
            self.simulation_engine.reset()
            self.simulation_timer.start(50)  # 20 FPS
            
    def stop_simulation(self):
        """Stop circuit simulation"""
        if self.simulation_running:
            self.simulation_running = False
            self.simulation_timer.stop()
            
    def update_simulation(self):
        """Update simulation step and visuals"""
        # Run simulation step
        self.simulation_engine.step(0.05)  # 50ms time step
        
        # Update component visuals
        for comp_id, graphics_item in self.component_items.items():
            graphics_item.update_state()
            
        # Update wire visuals
        for wire_item in self.wire_items:
            connection = wire_item.connection
            # Get current from source pin
            from_comp = self.circuit.get_component(connection.from_component)
            if from_comp:
                from_pin = from_comp.get_pin(connection.from_pin)
                if from_pin:
                    wire_item.update_current(from_pin.current)
                    
    def clear(self):
        """Clear all components and connections"""
        self.stop_simulation()
        self.scene.clear()
        self.component_items.clear()
        self.wire_items.clear()
        self.circuit = Circuit()
        self.simulation_engine = SimulationEngine(self.circuit)
        self.setup_canvas()
