# MeteoApp Translation System Configuration
# This file contains configuration options for the translation system

# Quick Start Guide for Developers
# ================================

## 1. Basic Usage
# Import the translation manager:
from src.translations import translation_manager

# Get a translation:
text = translation_manager.get_translation('weather.conditions.sunny')

# Get translation with fallback:
text = translation_manager.get_translation('new.key', 'Default Text')

## 2. Language Management
# Change language:
translation_manager.set_current_language('it')

# Get current language:
current_lang = translation_manager.get_current_language()

# Get available languages:
languages = translation_manager.get_supported_languages()

## 3. Backward Compatibility
# The system automatically maps old paths to new modules:
# OLD: translation_service.get('dashboard_widgets_temperature_title')
# NEW: Automatically mapped to 'charts.temperature_chart_items.temperature_chart_title'

## 4. Adding New Translations
# To add new translations, edit the appropriate module file:
# - src/translations/modules/navigation.py (menus, navigation)
# - src/translations/modules/weather.py (weather conditions, forecasts)
# - src/translations/modules/air_quality.py (air quality indicators)
# - src/translations/modules/settings.py (app settings, preferences)
# - src/translations/modules/charts.py (charts, graphs, visualizations)
# - src/translations/modules/alerts.py (notifications, warnings)

## 5. Translation Key Structure
# Keys follow a hierarchical structure: module.section.key
# Example: 'weather.conditions.sunny' → weather module, conditions section, sunny key

## 6. Management Utility
# Use translation_manager.py for various management tasks:
# python translation_manager.py --stats          # Show statistics
# python translation_manager.py --validate       # Check completeness
# python translation_manager.py --search "term"  # Search translations
# python translation_manager.py --export file.json  # Export to JSON

# Language Configuration
DEFAULT_LANGUAGE = 'en'
FALLBACK_LANGUAGE = 'en'

# Module Priority (for conflict resolution)
MODULE_PRIORITY = [
    'navigation',    # Highest priority
    'weather',
    'air_quality',
    'settings',
    'charts',
    'units',         # Unit system translations
    'alerts'         # Lowest priority
]

# Cache Configuration
ENABLE_CACHE = True
CACHE_SIZE_LIMIT = 1000  # Maximum number of cached translations

# Debug Settings
DEBUG_MISSING_TRANSLATIONS = False  # Set to True to log missing keys
DEBUG_MODULE_LOADING = False        # Set to True to log module loading

# Performance Monitoring
TRACK_TRANSLATION_USAGE = False     # Set to True to track most used translations
PERFORMANCE_LOGGING = False         # Set to True to log performance metrics

# RTL Language Support
RTL_LANGUAGES = ['ar']  # Languages that require right-to-left text direction

# Translation Validation Rules
VALIDATION_RULES = {
    'require_all_languages': True,      # All keys must have all language variants
    'allow_empty_strings': False,       # Prevent empty translation strings
    'max_length_warnings': {            # Warn if translations exceed these lengths
        'navigation': 50,
        'weather': 100,
        'air_quality': 80,
        'settings': 60,
        'charts': 70,
        'units': 40,                    # Unit translations are typically short
        'alerts': 150
    }
}
