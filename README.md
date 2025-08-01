# PGN Comment Translator

A simple CLI tool to translate comments in PGN (Portable Game Notation) chess files using LibreTranslate API.

## Features

- Translates only PGN comments while preserving valid structure
- Compatible with public or local LibreTranslate APIs
- Support for API keys (for instances that require them)
- Flexible configuration via environment variables or CLI arguments
- Preserves original PGN format
- Robust error handling

## Installation

### Option 1: Quick install
```bash
git clone https://github.com/your-username/pgn-comment-translator.git
cd pgn-comment-translator
pip install -r requirements.txt
chmod +x pgn_translator.py
```

### Option 2: With virtual environment
```bash
git clone https://github.com/your-username/pgn-comment-translator.git
cd pgn-comment-translator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
chmod +x pgn_translator.py
```

## Configuration

### Environment variables (recommended)

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```bash
# LibreTranslate API URL
LIBRETRANSLATE_URL=http://localhost:5000

# API Key (optional, only if your instance requires it)
LIBRETRANSLATE_API_KEY=your_api_key_here

# Default languages
DEFAULT_SOURCE_LANG=en
DEFAULT_TARGET_LANG=es

# Request timeout
REQUEST_TIMEOUT=30
```

### Popular public instances

- **LibreTranslate.de**: `https://libretranslate.de` (no API key required)
- **LibreTranslate.org**: `https://libretranslate.org` (no API key required)
- **Local instance**: `http://localhost:5000` (default configuration)

## Usage

### Basic commands

```bash
# Use configuration from .env file
./pgn_translator.py input.pgn output.pgn

# With specific parameters
./pgn_translator.py input.pgn output.pgn --source en --target es

# With specific API
./pgn_translator.py input.pgn output.pgn --api-url https://libretranslate.de

# With API key
./pgn_translator.py input.pgn output.pgn --api-key your_api_key

# Test connection
./pgn_translator.py --test-connection
```

### Available options

- `input_file`: Input PGN file
- `output_file`: Output PGN file  
- `--source`, `-s`: Source language
- `--target`, `-t`: Target language
- `--api-url`: LibreTranslate API URL
- `--api-key`: API Key (if required)
- `--test-connection`: Only test API connection

## Configuration examples for GitHub

### For local development
```bash
# .env
LIBRETRANSLATE_URL=http://localhost:5000
DEFAULT_SOURCE_LANG=en
DEFAULT_TARGET_LANG=es
```

### For use with public API
```bash
# .env
LIBRETRANSLATE_URL=https://libretranslate.de
DEFAULT_SOURCE_LANG=en
DEFAULT_TARGET_LANG=es
```

### For instance with API key
```bash
# .env (DO NOT commit this file)
LIBRETRANSLATE_URL=https://api.myprovider.com
LIBRETRANSLATE_API_KEY=sk-123456789abcdef
DEFAULT_SOURCE_LANG=en
DEFAULT_TARGET_LANG=fr
```

## Setting up LibreTranslate

### Local with Docker
```bash
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate
```

### From source
```bash
git clone https://github.com/LibreTranslate/LibreTranslate
cd LibreTranslate
pip install -e .
libretranslate
```

## Example

Original file `example.pgn`:
```
1. e4 {A strong opening move} c5 {The Sicilian Defense}
```

After translation (en→es):
```
1. e4 {Un movimiento de apertura fuerte} c5 {La Defensa Siciliana}
```

## Common language codes

- `en`: English
- `es`: Spanish  
- `fr`: French
- `de`: German
- `it`: Italian
- `pt`: Portuguese
- `ru`: Russian
- `zh`: Chinese
- `ja`: Japanese
- `ar`: Arabic

## Troubleshooting

1. **Connection error**: Verify LibreTranslate is running
2. **Comments not translated**: Check language codes
3. **Corrupted file**: The script preserves original PGN structure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) for the translation API
- Chess community for PGN format standards

## Ejemplo

Archivo original `example.pgn`:
```
1. e4 {A strong opening move} c5 {The Sicilian Defense}
```

Después de traducir (en→es):
```
1. e4 {Un movimiento de apertura fuerte} c5 {La Defensa Siciliana}
```

## Códigos de idioma comunes

- `en`: Inglés
- `es`: Español  
- `fr`: Francés
- `de`: Alemán
- `it`: Italiano
- `pt`: Portugués
- `ru`: Ruso
- `zh`: Chino

## Solución de problemas

1. **Error de conexión**: Verificar que LibreTranslate esté ejecutándose
2. **Comentarios no traducidos**: Verificar códigos de idioma
3. **Archivo corrupto**: El script preserva la estructura PGN original