#!/usr/bin/env python3
"""
PGN Comment Translator - Translates comments in PGN chess files using LibreTranslate API
"""

import re
import json
import requests
import argparse
import sys
import os
from typing import List, Tuple, Optional
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class PGNTranslator:
    def __init__(self, api_url: str = None, api_key: str = None, timeout: int = None):
        # Try offline first, then web service
        self.api_url = (api_url or os.getenv('LIBRETRANSLATE_URL', self._get_default_api_url())).rstrip('/')
        self.api_key = api_key or os.getenv('LIBRETRANSLATE_API_KEY')
        self.timeout = timeout or int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.translate_endpoint = f"{self.api_url}/translate"
        self.is_offline = self._is_offline_mode()
        
        # Print mode info
        if self.is_offline:
            print(f"🔧 Using offline LibreTranslate: {self.api_url}")
        else:
            print(f"🌐 Using web LibreTranslate: {self.api_url}")
            
        # Handle API key for web service
        if not self.is_offline and not self.api_key:
            self._prompt_for_api_key()
    
    def _get_default_api_url(self) -> str:
        """Try offline first, fallback to web service"""
        # Try offline first
        offline_url = "http://localhost:5000"
        try:
            response = requests.get(f"{offline_url}/languages", timeout=3)
            if response.status_code == 200:
                return offline_url
        except requests.RequestException:
            pass
        
        # Fallback to web service
        return "https://libretranslate.com"
    
    def _is_offline_mode(self) -> bool:
        """Check if using offline LibreTranslate"""
        return 'localhost' in self.api_url or '127.0.0.1' in self.api_url
    
    def _prompt_for_api_key(self):
        """Prompt user for API key if not configured"""
        print("\n⚠️  LibreTranslate web service requires an API key.")
        print("Get your free API key at: https://libretranslate.com/")
        print("\n💡 Tip: To use offline, install LibreTranslate locally and it will be auto-detected")
        print("   pip install libretranslate")
        print("   libretranslate")
        print("\nOptions to configure your API key:")
        print("1. Set LIBRETRANSLATE_API_KEY environment variable")
        print("2. Create .env file with LIBRETRANSLATE_API_KEY=your_key")
        print("3. Use --api-key parameter")
        
        response = input("\nDo you want to enter your API key now? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            api_key = input("Enter your LibreTranslate API key: ").strip()
            if api_key:
                self.api_key = api_key
                print("✓ API key configured for this session")
            else:
                print("❌ No API key entered. Exiting...")
                sys.exit(1)
        else:
            print("❌ API key required for LibreTranslate web service. Exiting...")
            sys.exit(1)
    
    def extract_comments(self, pgn_content: str) -> List[Tuple[str, int, int]]:
        """Extract comments from PGN and their positions"""
        comments = []
        pattern = r'\{([^}]+)\}'
        
        for match in re.finditer(pattern, pgn_content):
            comment_text = match.group(1)
            start_pos = match.start()
            end_pos = match.end()
            comments.append((comment_text, start_pos, end_pos))
        
        return comments
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text using LibreTranslate API"""
        try:
            payload = {
                "q": text,
                "source": source_lang,
                "target": target_lang
            }
            
            if self.api_key:
                payload["api_key"] = self.api_key
            elif not self.is_offline:
                print("⚠️  Warning: No API key provided for web service", file=sys.stderr)
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.translate_endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("translatedText", text)
            else:
                print(f"Translation error: {response.status_code} - {response.text}", file=sys.stderr)
                return text
                
        except requests.RequestException as e:
            print(f"Connection error: {e}", file=sys.stderr)
            return text
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}", file=sys.stderr)
            return text
    
    def translate_pgn(self, pgn_content: str, source_lang: str, target_lang: str) -> str:
        """Translate all comments in a PGN file"""
        comments = self.extract_comments(pgn_content)
        
        if not comments:
            print("No comments found to translate")
            return pgn_content
        
        print(f"Found {len(comments)} comments to translate...")
        
        # Translate from back to front to maintain positions
        translated_content = pgn_content
        
        for i, (comment_text, start_pos, end_pos) in enumerate(reversed(comments)):
            print(f"Translating comment {len(comments) - i}/{len(comments)}: {comment_text[:50]}...")
            
            translated_text = self.translate_text(comment_text, source_lang, target_lang)
            
            if translated_text and translated_text != comment_text:
                # Replace original comment with translation
                translated_content = (
                    translated_content[:start_pos] + 
                    f"{{{translated_text}}}" + 
                    translated_content[end_pos:]
                )
        
        return translated_content
    
    def test_connection(self) -> bool:
        """Test connection with LibreTranslate API"""
        try:
            test_payload = {
                "q": "test",
                "source": "en",
                "target": "es"
            }
            
            if self.api_key and not self.is_offline:
                test_payload["api_key"] = self.api_key
            
            response = requests.post(
                self.translate_endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(test_payload),
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code == 403 and not self.is_offline:
                print("❌ API key invalid or required for web service", file=sys.stderr)
                return False
            else:
                print(f"❌ Connection test failed: {response.status_code}", file=sys.stderr)
                return False
            
        except requests.RequestException as e:
            if self.is_offline:
                print("❌ Cannot connect to offline LibreTranslate. Make sure it's running:", file=sys.stderr)
                print("   pip install libretranslate", file=sys.stderr)
                print("   libretranslate", file=sys.stderr)
            else:
                print(f"❌ Connection error: {e}", file=sys.stderr)
            return False

def main():
    # Default values from environment variables
    default_source = os.getenv('DEFAULT_SOURCE_LANG', 'en')
    default_target = os.getenv('DEFAULT_TARGET_LANG', 'es')
    # No default URL - let the class auto-detect
    default_api_url = os.getenv('LIBRETRANSLATE_URL')
    
    parser = argparse.ArgumentParser(description="Translate comments in PGN chess files using LibreTranslate API")
    
    parser.add_argument("input_file", nargs='?', help="Input PGN file")
    parser.add_argument("output_file", nargs='?', help="Output PGN file")
    parser.add_argument("--source", "-s", default=default_source, help=f"Source language (default: {default_source})")
    parser.add_argument("--target", "-t", default=default_target, help=f"Target language (default: {default_target})")
    parser.add_argument("--api-url", default=default_api_url, help="LibreTranslate API URL (auto-detects offline/web)")
    parser.add_argument("--api-key", help="LibreTranslate API key (required for web service)")
    parser.add_argument("--test-connection", action="store_true", help="Test API connection and exit")
    parser.add_argument("--offline", action="store_true", help="Force offline mode (localhost:5000)")
    parser.add_argument("--web", action="store_true", help="Force web mode (libretranslate.com)")
    
    args = parser.parse_args()
    
    # Handle force mode flags
    if args.offline and args.web:
        parser.error("Cannot use both --offline and --web flags")
    
    api_url = args.api_url
    if args.offline:
        api_url = "http://localhost:5000"
    elif args.web:
        api_url = "https://libretranslate.com"
    
    translator = PGNTranslator(api_url, args.api_key)
    
    if args.test_connection:
        if translator.test_connection():
            if translator.is_offline:
                print("✓ Successful connection to offline LibreTranslate")
            else:
                print("✓ Successful connection to web LibreTranslate")
            sys.exit(0)
        else:
            print("✗ Connection error with LibreTranslate")
            sys.exit(1)
    
    # Verify required arguments for translation
    if not args.test_connection and (not args.input_file or not args.output_file):
        parser.error("input_file and output_file arguments are required (except with --test-connection)")
    
    # Verify files
    if not args.test_connection:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: File '{args.input_file}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        output_path = Path(args.output_file)
    
    # Test connection
    print("Testing connection to LibreTranslate...")
    if not translator.test_connection():
        print("Error: Cannot connect to LibreTranslate. Verify it's running.", file=sys.stderr)
        sys.exit(1)
    
    print("✓ Connection successful")
    
    # Read PGN file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            pgn_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Translate
    print(f"Translating from {args.source} to {args.target}...")
    translated_content = translator.translate_pgn(pgn_content, args.source, args.target)
    
    # Save result
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"✓ Translation completed. File saved to: {args.output_file}")
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()