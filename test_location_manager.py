#!/usr/bin/env python3
"""
Test script per le traduzioni del Location Manager Dialog.
"""
import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from translations import translation_manager


def test_location_manager_translations():
    """Test le traduzioni del location manager dialog."""
    
    print("=== Testing Location Manager Dialog Translations ===\n")
    
    # Test con diverse lingue
    languages_to_test = ["en", "it", "fr", "de", "es"]
    
    # Chiavi principali del dialog
    main_keys = [
        'title', 'dialog_title', 'description', 'add_location', 'saved_locations',
        'city_label', 'search_button', 'searching', 'add_button', 'use_current',
        'stats', 'export', 'import'
    ]
    
    # New message keys
    message_keys = [
        'no_locations_found', 'search_error', 'location_added_successfully',
        'location_already_exists', 'error_adding_location', 'location_removed',
        'confirm_delete', 'delete_button', 'select_button'
    ]
    
    # Empty state keys  
    empty_keys = [
        'no_saved_locations', 'add_location_to_start'
    ]
    
    for lang in languages_to_test:
        print(f"--- Testing language: {lang.upper()} ---")
        
        print("Main dialog keys:")
        for key in main_keys:
            try:
                translation = translation_manager.get_translation("weather", "location_manager_dialog", key, lang)
                print(f"  {key}: {translation}")
            except Exception as e:
                print(f"  {key}: ERROR - {e}")
        
        print("\nMessage keys:")
        for key in message_keys:
            try:
                translation = translation_manager.get_translation("weather", "location_manager_dialog", key, lang)
                print(f"  {key}: {translation}")
            except Exception as e:
                print(f"  {key}: ERROR - {e}")
        
        print("\nEmpty state keys:")
        for key in empty_keys:
            try:
                translation = translation_manager.get_translation("weather", "location_manager_dialog", key, lang)
                print(f"  {key}: {translation}")
            except Exception as e:
                print(f"  {key}: ERROR - {e}")
        
        # Test dialog buttons
        print("\nDialog buttons:")
        try:
            close = translation_manager.get_translation("weather", "dialog_buttons", "close", lang)
            print(f"  close: {close}")
        except Exception as e:
            print(f"  close: ERROR - {e}")
        
        print("\n" + "="*60 + "\n")
    
    print("Location Manager Dialog translation test completed!")


if __name__ == "__main__":
    test_location_manager_translations()
