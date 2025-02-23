# Site-Parser# Site Parser

A powerful web crawler and word finder that searches websites for specific words or phrases and provides detailed location information.

## Features

- Single word search
- Dictionary-based search
- File-based word list search
- Multi-threaded crawling
- Export results to CSV and JSON
- Detailed scan reports
- Context-aware word finding
- Respects robots.txt and site load
- Smart encoding detection
- Progress tracking
- ASCII art interface

## Requirements

Required packages:
- requests
- beautifulsoup4

## Installation

1. Clone the repository:

## Usage

Run the script:
```bash
python main.py
```

### Search Modes

1. **Single Word Search**
   - Choose option [1]
   - Enter website URL
   - Enter single word to search
   - Set maximum pages to scan

2. **Dictionary Search**
   - Choose option [2]
   - Enter website URL
   - Enter words one by one
   - Press Enter twice to finish
   - Set maximum pages to scan

3. **File-based Search**
   - Choose option [3]
   - Enter website URL
   - Provide path to word list file
   - Set maximum pages to scan

### Word List File Format

Create a text file with words to search (one per line):
```
word1
word2
word3
```

### Export Options

Results can be exported in:
- CSV format
- JSON format
- Both formats simultaneously

## Example

```python
# Example word list (words.txt):
Python
programming
development
code
interpreter
variable
function
class
object
module
library
framework

# Example URL:
https://en.wikipedia.org/wiki/Python_(programming_language)
```

## Output Format

### CSV Output
```csv
Word,URL,Location
Python,https://example.com,In tag <p>: Context of found word...
```

### JSON Output
```json
{
    "word": {
        "url": [
            "In tag <p>: Context of found word..."
        ]
    }
}
```

## Limitations

- Respects website robots.txt
- 0.5-second delay between requests
- Maximum 3 concurrent threads
- Default limit of 50 pages per scan

## Error Handling

- Network error handling
- File reading error handling
- Invalid URL handling
- Encoding detection
- Timeout management

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Your Name
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## Acknowledgments

- BeautifulSoup4 for HTML parsing
- Requests library for HTTP requests


