"""
Arduino CLI Manager
Wrapper for Arduino CLI operations
"""

import subprocess
import json
import os
from typing import List, Dict, Optional
from pathlib import Path


class ArduinoCLI:
    """Wrapper for Arduino CLI operations"""
    
    def __init__(self, cli_path: Optional[str] = None):
        self.cli_path = cli_path or os.getenv('ARDUINO_CLI_PATH', 'arduino-cli')
        self.available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if Arduino CLI is available"""
        try:
            result = subprocess.run(
                [self.cli_path, 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"Arduino CLI found: {result.stdout.strip()}")
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print("Arduino CLI not found - hardware features disabled")
            print("Install with: brew install arduino-cli")
        return False
    
    def list_boards(self) -> List[Dict]:
        """List all available board types"""
        if not self.available:
            return []
            
        try:
            result = subprocess.run(
                [self.cli_path, 'board', 'listall', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return json.loads(result.stdout).get('boards', [])
        except Exception as e:
            print(f"Error listing boards: {e}")
            return []
    
    def list_connected_boards(self) -> List[Dict]:
        """List connected Arduino/ESP32 boards"""
        if not self.available:
            return []
            
        try:
            result = subprocess.run(
                [self.cli_path, 'board', 'list', '--format', 'json'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error listing connected boards: {e}")
            return []
    
    def compile_sketch(self, sketch_path: str, fqbn: str) -> Dict:
        """Compile an Arduino sketch"""
        if not self.available:
            return {'success': False, 'error': 'Arduino CLI not available'}
            
        try:
            result = subprocess.run(
                [self.cli_path, 'compile', '--fqbn', fqbn, sketch_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=60
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upload_sketch(self, sketch_path: str, fqbn: str, port: str) -> Dict:
        """Upload compiled sketch to board"""
        if not self.available:
            return {'success': False, 'error': 'Arduino CLI not available'}
            
        try:
            result = subprocess.run(
                [self.cli_path, 'upload', '--fqbn', fqbn, '--port', port, sketch_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=60
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr}
        except Exception as e:
            return {'success': False, 'error': str(e)}
