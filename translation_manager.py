#!/usr/bin/env python3
"""
Translation Management Utility for MeteoApp.
Provides tools for managing, validating, and expanding the modular translation system.
"""

import os
import sys
import json
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from translations import translation_manager
from translations.languages import get_all_language_codes


class TranslationUtility:
    """Utility class for managing translations in MeteoApp."""
    
    def __init__(self):
        self.manager = translation_manager
        self.all_languages = get_all_language_codes()
    
    def find_missing_translations(self) -> Dict[str, List[str]]:
        """Find missing translations across all modules."""
        missing = {}
        
        for module_name, module_data in self.manager._loaded_modules.items():
            missing[module_name] = []
            
            for section_name, section_data in module_data.items():
                for key, translations in section_data.items():
                    if isinstance(translations, dict):
                        missing_langs = []
                        for lang in self.all_languages:
                            if lang not in translations:
                                missing_langs.append(lang)
                        
                        if missing_langs:
                            missing[module_name].append({
                                'section': section_name,
                                'key': key,
                                'missing_languages': missing_langs
                            })
        
        return missing
    
    def generate_translation_template(self, text_en: str, key: str) -> Dict[str, str]:
        """Generate a template for a new translation key."""
        template = {}
        for lang in self.all_languages:
            if lang == 'en':
                template[lang] = text_en
            else:
                template[lang] = f"[{lang.upper()}] {text_en}"  # Placeholder
        return template
    
    def validate_translation_completeness(self) -> Dict[str, Any]:
        """Validate that all translations are complete."""
        report = {
            'total_keys': 0,
            'complete_keys': 0,
            'incomplete_keys': 0,
            'missing_by_language': {lang: 0 for lang in self.all_languages},
            'details': []
        }
        
        for module_name, module_data in self.manager._loaded_modules.items():
            for section_name, section_data in module_data.items():
                for key, translations in section_data.items():
                    if isinstance(translations, dict):
                        report['total_keys'] += 1
                        
                        missing_langs = []
                        for lang in self.all_languages:
                            if lang not in translations or not translations[lang]:
                                missing_langs.append(lang)
                                report['missing_by_language'][lang] += 1
                        
                        if missing_langs:
                            report['incomplete_keys'] += 1
                            report['details'].append({
                                'module': module_name,
                                'section': section_name,
                                'key': key,
                                'missing': missing_langs
                            })
                        else:
                            report['complete_keys'] += 1
        
        return report
    
    def export_translations_to_json(self, output_file: str = "translations_export.json"):
        """Export all translations to a JSON file for external editing."""
        export_data = {
            'metadata': {
                'languages': self.all_languages,
                'modules': list(self.manager._loaded_modules.keys()),
                'total_keys': 0
            },
            'translations': {}
        }
        
        total_keys = 0
        for module_name, module_data in self.manager._loaded_modules.items():
            export_data['translations'][module_name] = module_data
            for section_data in module_data.values():
                total_keys += len(section_data)
        
        export_data['metadata']['total_keys'] = total_keys
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {total_keys} translation keys to {output_file}")
    
    def search_translations(self, search_term: str, language: str = 'en') -> List[Dict[str, str]]:
        """Search for translations containing a specific term."""
        results = []
        
        for module_name, module_data in self.manager._loaded_modules.items():
            for section_name, section_data in module_data.items():
                for key, translations in section_data.items():
                    if isinstance(translations, dict) and language in translations:
                        if search_term.lower() in translations[language].lower():
                            results.append({
                                'module': module_name,
                                'section': section_name,
                                'key': key,
                                'text': translations[language],
                                'full_path': f"{module_name}.{section_name}.{key}"
                            })
        
        return results
    
    def print_usage_statistics(self):
        """Print detailed usage statistics."""
        stats = self.manager.get_translation_stats()
        
        print("\n🌐 MeteoApp Translation System Statistics")
        print("=" * 50)
        print(f"📦 Total Modules: {stats['modules']}")
        print(f"🌍 Supported Languages: {stats['languages']}")
        print(f"🔧 Total Translation Keys: {sum(info['total_keys'] for info in stats['module_breakdown'].values())}")
        
        print("\n📊 Module Breakdown:")
        for module, info in stats['module_breakdown'].items():
            print(f"   • {module:12} → {info['sections']:2} sections, {info['total_keys']:3} keys")
        
        # Completeness report
        completeness = self.validate_translation_completeness()
        completion_rate = (completeness['complete_keys'] / completeness['total_keys'] * 100) if completeness['total_keys'] > 0 else 0
        
        print(f"\n✅ Translation Completeness: {completion_rate:.1f}%")
        print(f"   Complete keys: {completeness['complete_keys']}")
        print(f"   Incomplete keys: {completeness['incomplete_keys']}")
        
        if completeness['incomplete_keys'] > 0:
            print("\n⚠️  Missing Translations by Language:")
            for lang, count in completeness['missing_by_language'].items():
                if count > 0:
                    print(f"   • {lang}: {count} missing")


def main():
    """Main function for the translation utility."""
    import argparse
    
    parser = argparse.ArgumentParser(description='MeteoApp Translation Management Utility')
    parser.add_argument('--stats', action='store_true', help='Show translation statistics')
    parser.add_argument('--validate', action='store_true', help='Validate translation completeness')
    parser.add_argument('--export', type=str, help='Export translations to JSON file')
    parser.add_argument('--search', type=str, help='Search for translations containing text')
    parser.add_argument('--lang', type=str, default='en', help='Language for search (default: en)')
    parser.add_argument('--missing', action='store_true', help='Find missing translations')
    
    args = parser.parse_args()
    
    utility = TranslationUtility()
    
    if args.stats:
        utility.print_usage_statistics()
    
    if args.validate:
        print("\n🔍 Validating Translation Completeness...")
        report = utility.validate_translation_completeness()
        completion_rate = (report['complete_keys'] / report['total_keys'] * 100) if report['total_keys'] > 0 else 0
        print(f"✅ Completion Rate: {completion_rate:.1f}%")
        
        if report['incomplete_keys'] > 0:
            print(f"\n⚠️  Found {report['incomplete_keys']} incomplete translations:")
            for detail in report['details'][:10]:  # Show first 10
                print(f"   • {detail['module']}.{detail['section']}.{detail['key']} → Missing: {', '.join(detail['missing'])}")
            if len(report['details']) > 10:
                print(f"   ... and {len(report['details']) - 10} more")
    
    if args.export:
        utility.export_translations_to_json(args.export)
    
    if args.search:
        print(f"\n🔍 Searching for '{args.search}' in {args.lang} translations...")
        results = utility.search_translations(args.search, args.lang)
        print(f"Found {len(results)} matches:")
        for result in results[:20]:  # Show first 20
            print(f"   • {result['full_path']} → \"{result['text']}\"")
        if len(results) > 20:
            print(f"   ... and {len(results) - 20} more")
    
    if args.missing:
        print("\n🔍 Finding Missing Translations...")
        missing = utility.find_missing_translations()
        for module, missing_list in missing.items():
            if missing_list:
                print(f"\n📦 {module}:")
                for item in missing_list[:5]:  # Show first 5 per module
                    print(f"   • {item['section']}.{item['key']} → Missing: {', '.join(item['missing_languages'])}")
                if len(missing_list) > 5:
                    print(f"   ... and {len(missing_list) - 5} more")
    
    # If no arguments, show help
    if not any(vars(args).values()):
        utility.print_usage_statistics()
        print("\n💡 Use --help to see available options")


if __name__ == "__main__":
    main()
