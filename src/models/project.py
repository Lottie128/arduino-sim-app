"""
Project data model
"""

from dataclasses import dataclass, field
from typing import Optional
from .circuit import Circuit


@dataclass
class Project:
    """Project containing circuit and code"""
    circuit: Circuit = field(default_factory=Circuit)
    arduino_code: str = ""
    filename: Optional[str] = None
    is_modified: bool = False
    board_type: str = "arduino:avr:uno"
    board_port: Optional[str] = None
    
    def mark_modified(self):
        """Mark project as modified"""
        self.is_modified = True
        
    def mark_saved(self):
        """Mark project as saved"""
        self.is_modified = False
