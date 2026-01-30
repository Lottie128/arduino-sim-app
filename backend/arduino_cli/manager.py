import subprocess
import json
import os
from typing import List, Dict, Optional
from pathlib import Path

class ArduinoManager:
    """Wrapper for Arduino CLI operations"""
    
    def __init__(self, cli_path: Optional[str] = None):
        self.cli_path = cli_path or os.getenv('ARDUINO_CLI_PATH', 'arduino-cli')
        self._verify_cli()
    
    def _verify_cli(self):
        """Verify Arduino CLI is installed and accessible"""
        try:
            result = subprocess.run(
                [self.cli_path, 'version'],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Arduino CLI version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"Arduino CLI not found or not working: {e}")
    
    def list_boards(self) -> List[Dict]:
        """List all available board types"""
        result = subprocess.run(
            [self.cli_path, 'board', 'listall', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout).get('boards', [])
    
    def list_connected_boards(self) -> List[Dict]:
        """List connected Arduino/ESP32 boards"""
        result = subprocess.run(
            [self.cli_path, 'board', 'list', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    
    def compile_sketch(self, sketch_path: str, fqbn: str) -> Dict:
        """Compile an Arduino sketch
        
        Args:
            sketch_path: Path to sketch directory or .ino file
            fqbn: Fully Qualified Board Name (e.g., 'arduino:avr:uno')
        """
        try:
            result = subprocess.run(
                [self.cli_path, 'compile', '--fqbn', fqbn, sketch_path, '--format', 'json'],
                capture_output=True,
                text=True,
                check=True
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr}
    
    def upload_sketch(self, sketch_path: str, fqbn: str, port: str) -> Dict:
        """Upload compiled sketch to board
        
        Args:
            sketch_path: Path to sketch directory
            fqbn: Fully Qualified Board Name
            port: Serial port (e.g., '/dev/ttyUSB0' or 'COM3')
        """
        try:
            result = subprocess.run(
                [self.cli_path, 'upload', '--fqbn', fqbn, '--port', port, sketch_path],
                capture_output=True,
                text=True,
                check=True
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr}
    
    def install_library(self, library_name: str) -> Dict:
        """Install an Arduino library"""
        try:
            result = subprocess.run(
                [self.cli_path, 'lib', 'install', library_name],
                capture_output=True,
                text=True,
                check=True
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr}
    
    def list_libraries(self) -> List[Dict]:
        """List installed libraries"""
        result = subprocess.run(
            [self.cli_path, 'lib', 'list', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout).get('installed_libraries', [])
    
    def search_libraries(self, query: str) -> List[Dict]:
        """Search for libraries in Arduino Library Manager"""
        result = subprocess.run(
            [self.cli_path, 'lib', 'search', query, '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout).get('libraries', [])
