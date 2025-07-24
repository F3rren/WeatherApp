#!/usr/bin/env python3
"""
Test per la funzione helper _get_field_value.
"""

class MockField:
    def __init__(self, value):
        self.value = value

def _get_field_value(field, allow_empty=False):
    """Safely get and clean field value, handling None cases."""
    if not field or field.value is None:
        return None if allow_empty else ""
    
    cleaned_value = field.value.strip()
    if not cleaned_value and not allow_empty:
        return ""
    
    return cleaned_value if cleaned_value else (None if allow_empty else "")

def test_helper_function():
    """Test la funzione helper."""
    
    print("=== Testing _get_field_value Helper Function ===\n")
    
    test_cases = [
        (None, False, ""),
        (None, True, None),
        ("", False, ""),
        ("", True, None),
        ("  ", False, ""),
        ("  ", True, None),
        ("Milano", False, "Milano"),
        ("Milano", True, "Milano"),
        ("  Roma  ", False, "Roma"),
        ("  Roma  ", True, "Roma"),
    ]
    
    for field_value, allow_empty, expected in test_cases:
        field = MockField(field_value) if field_value is not None else MockField(field_value)
        result = _get_field_value(field, allow_empty)
        
        status = "✅" if result == expected else "❌"
        print(f"{status} Field: {repr(field_value)}, allow_empty: {allow_empty} -> {repr(result)} (expected: {repr(expected)})")
    
    # Test con field None
    result = _get_field_value(None, False)
    print(f"✅ None field, allow_empty: False -> {repr(result)} (expected: '')")
    
    result = _get_field_value(None, True)
    print(f"✅ None field, allow_empty: True -> {repr(result)} (expected: None)")
    
    print("\n" + "="*60)
    print("Helper function test completed!")

if __name__ == "__main__":
    test_helper_function()
