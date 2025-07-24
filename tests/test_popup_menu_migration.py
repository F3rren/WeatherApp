"""
Test per verificare la migrazione del popup menu al sistema modulare di traduzioni.
"""
import unittest
import sys
import os

# Aggiungi la directory src al path per importare i moduli
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from translations import translation_manager

class TestPopupMenuMigration(unittest.TestCase):
    """Test per la migrazione delle traduzioni del popup menu."""
    
    def setUp(self):
        """Setup test environment."""
        self.languages = ["en", "it", "es", "fr", "de", "pt", "ru", "zh", "ja", "ko", "ar", "hi", "id"]
        self.popup_items = [
            "weather", "maps", "advanced_maps", "interactive_maps", 
            "satellite_view", "radar_live", "analytics", "weather_trends", 
            "historical_data", "alerts", "push_notifications", "tools", 
            "location_manager", "export_data", "settings"
        ]
    
    def test_popup_menu_module_loaded(self):
        """Test che il modulo popup_menu sia caricato correttamente."""
        self.assertIn("popup_menu", translation_manager._loaded_modules, 
                     "Il modulo popup_menu dovrebbe essere caricato")
    
    def test_all_popup_items_available(self):
        """Test che tutti gli elementi del popup menu abbiano traduzioni."""
        for item in self.popup_items:
            with self.subTest(item=item):
                for lang in self.languages:
                    with self.subTest(language=lang):
                        translation = translation_manager.get_translation(
                            "popup_menu", "items", item, lang
                        )
                        self.assertIsNotNone(translation, 
                                           f"Traduzione mancante per {item} in {lang}")
                        self.assertNotEqual(translation, "", 
                                          f"Traduzione vuota per {item} in {lang}")
    
    def test_popup_menu_specific_translations(self):
        """Test traduzioni specifiche per alcuni elementi critici."""
        test_cases = [
            ("weather", "en", "Weather"),
            ("weather", "it", "Meteo"),
            ("maps", "en", "Maps"),
            ("maps", "it", "Mappe"),
            ("settings", "en", "Settings"),
            ("settings", "it", "Impostazioni"),
            ("alerts", "en", "Alerts"),
            ("alerts", "it", "Avvisi"),
        ]
        
        for item, lang, expected in test_cases:
            with self.subTest(item=item, lang=lang):
                translation = translation_manager.get_translation(
                    "popup_menu", "items", item, lang
                )
                self.assertEqual(translation, expected, 
                               f"Traduzione errata per {item} in {lang}")
    
    def test_indonesian_translations(self):
        """Test specifico per le traduzioni indonesiane."""
        indonesian_cases = [
            ("weather", "Cuaca"),
            ("maps", "Peta"),
            ("settings", "Pengaturan"),
            ("alerts", "Peringatan"),
        ]
        
        for item, expected in indonesian_cases:
            with self.subTest(item=item):
                translation = translation_manager.get_translation(
                    "popup_menu", "items", item, "id"
                )
                self.assertEqual(translation, expected, 
                               f"Traduzione indonesiana errata per {item}")
    
    def test_fallback_functionality(self):
        """Test che il fallback funzioni per lingue non supportate."""
        # Test con una lingua non supportata
        translation = translation_manager.get_translation(
            "popup_menu", "items", "weather", "xx"
        )
        # Dovrebbe tornare la traduzione inglese come fallback
        self.assertEqual(translation, "Weather", 
                        "Il fallback dovrebbe tornare la traduzione inglese")
    
    def test_invalid_item_handling(self):
        """Test gestione di elementi non esistenti."""
        translation = translation_manager.get_translation(
            "popup_menu", "items", "nonexistent_item", "en"
        )
        # Dovrebbe tornare la chiave originale o un valore di fallback
        self.assertIsNotNone(translation, 
                           "Dovrebbe gestire elementi non esistenti")

if __name__ == '__main__':
    unittest.main()
