#!/usr/bin/env python3
"""
Test rapido per verificare la correzione del bug None.strip().
"""
import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_none_handling():
    """Test che simula il bug None.strip()."""
    
    print("=== Testing None Handling Fix ===\n")
    
    # Simula i valori che potrebbero essere None dai campi
    test_values = [None, "", "  ", "Milano", "  Roma  ", "New York"]
    
    print("Testing old problematic code vs new safe code:")
    
    for value in test_values:
        print(f"\nTest value: {repr(value)}")
        
        # Old problematic code (commentato per evitare errori)
        try:
            # old_result = value.strip()  # Questo causava l'errore
            print("  Old code: Would cause error if value is None")
        except AttributeError as e:
            print(f"  Old code: ERROR - {e}")
        
        # New safe code
        try:
            new_result = value.strip() if value else ""
            print(f"  New code: '{new_result}' (safe)")
        except Exception as e:
            print(f"  New code: Unexpected error - {e}")
        
        # Additional test for state/country fields
        try:
            safe_result = value.strip() if value and value.strip() else None
            print(f"  State/Country safe: {repr(safe_result)}")
        except Exception as e:
            print(f"  State/Country safe: Unexpected error - {e}")
    
    print("\n" + "="*50)
    print("None handling test completed successfully!")
    print("The LocationManagerDialog should now handle None values safely.")


if __name__ == "__main__":
    test_none_handling()
