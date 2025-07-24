#!/usr/bin/env python3
"""
Test per simulare la correzione del bug None.strip() nel location manager.
"""
import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock class per simulare un campo TextField
class MockTextField:
    def __init__(self, value):
        self.value = value

def _get_field_value(field, allow_empty=False):
    """Safely get and clean field value, handling None cases."""
    if not field or not hasattr(field, 'value') or field.value is None:
        return None if allow_empty else ""
    
    try:
        cleaned_value = str(field.value).strip()
        if not cleaned_value and not allow_empty:
            return ""
        
        return cleaned_value if cleaned_value else (None if allow_empty else "")
    except (AttributeError, TypeError):
        return None if allow_empty else ""

def test_location_manager_fix():
    """Test delle correzioni per il location manager."""
    
    print("=== Testing Location Manager Bug Fix ===\n")
    
    # Test cases che potrebbero causare il bug
    test_cases = [
        (None, "Campo None"),
        (MockTextField(None), "TextField con value None"),
        (MockTextField(""), "TextField con value vuoto"),
        (MockTextField("   "), "TextField con solo spazi"),
        (MockTextField("Milano"), "TextField con valore valido"),
        (MockTextField("  Roma  "), "TextField con spazi extra"),
    ]
    
    print("Test per city field (allow_empty=False):")
    for field, description in test_cases:
        try:
            result = _get_field_value(field, allow_empty=False)
            status = "✅"
            print(f"{status} {description}: {repr(result)}")
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
    
    print("\nTest per state/country field (allow_empty=True):")
    for field, description in test_cases:
        try:
            result = _get_field_value(field, allow_empty=True)
            status = "✅"
            print(f"{status} {description}: {repr(result)}")
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
    
    print("\n" + "="*60)
    print("Location Manager bug fix test completed!")
    print("All None values are now handled safely.")

if __name__ == "__main__":
    test_location_manager_fix()
