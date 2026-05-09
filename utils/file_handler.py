"""
File handling utility for data persistence.

This module demonstrates file I/O operations and error handling
patterns that students can learn from and extend.
"""

import json
import os
from typing import Any, Dict, List
from pathlib import Path


class FileHandler:
    """Handle file operations for data persistence."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_data(self, filename: str, data: Dict[str, Any]) -> None:
        """Save data to a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except (IOError, TypeError) as e:
            raise RuntimeError(f"Failed to save data to {filename}: {e}")
    
    def load_data(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load data from {filename}: {e}")
    
    def file_exists(self, filename: str) -> bool:
        """Check if a file exists in the data directory."""
        return (self.data_dir / filename).exists()
    
    def delete_file(self, filename: str) -> None:
        """Delete a file from the data directory."""
        filepath = self.data_dir / filename
        if filepath.exists():
            filepath.unlink()
    
    def list_files(self) -> list[str]:
        """List all files in the data directory."""
        return [f.name for f in self.data_dir.iterdir() if f.is_file()]
    
    def load_flashcards(self, filename: str) -> list[dict[str, str]]:
        """
        Load flashcard data from a JSON file with dual format support.
        
        Supports two JSON formats:
        - Array Format: [{"front": "API", "back": "Application Programming Interface"}, ...]
        - Object Format: {"cards": [{"front": "REST", "back": "Representational State Transfer"}, ...]}
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            List of flashcard dictionaries with 'front' and 'back' keys
            
        Raises:
            RuntimeError: For file not found, invalid JSON, missing fields, or format errors
        """
        filepath = self.data_dir / filename
        
        # Load and parse JSON file
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise RuntimeError(f"Flashcard file '{filename}' not found in data directory")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON format in '{filename}'. Please check for syntax errors: {e}")
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to read flashcard file '{filename}': {e}")
        
        # Determine format and extract cards
        cards_data = []
        if isinstance(data, list):
            # Array Format
            cards_data = data
        elif isinstance(data, dict) and 'cards' in data:
            # Object Format
            cards_data = data['cards']
            if not isinstance(cards_data, list):
                raise RuntimeError(f"Invalid format in '{filename}': 'cards' must be an array")
        else:
            raise RuntimeError(f"Invalid format in '{filename}': file must contain either an array of flashcards or an object with a 'cards' key")
        
        # Validate and sanitize flashcards
        validated_cards = []
        errors = []
        
        for i, card in enumerate(cards_data):
            if not isinstance(card, dict):
                errors.append(f"Flashcard at position {i + 1} must be an object")
                continue
            
            # Check for required fields
            if 'front' not in card:
                errors.append(f"Flashcard at position {i + 1} is missing required 'front' field")
                continue
            if 'back' not in card:
                errors.append(f"Flashcard at position {i + 1} is missing required 'back' field")
                continue
            
            # Validate and sanitize field values
            front = str(card['front']).strip() if card['front'] is not None else ''
            back = str(card['back']).strip() if card['back'] is not None else ''
            
            if not front:
                errors.append(f"Empty 'front' field found at flashcard {i + 1}")
                continue
            if not back:
                errors.append(f"Empty 'back' field found at flashcard {i + 1}")
                continue
            
            validated_cards.append({'front': front, 'back': back})
        
        # Report validation errors if any
        if errors:
            error_msg = f"Validation errors in '{filename}':\n" + '\n'.join(f"  - {error}" for error in errors)
            raise RuntimeError(error_msg)
        
        if not validated_cards:
            raise RuntimeError(f"No valid flashcards found in '{filename}'")
        
        return validated_cards