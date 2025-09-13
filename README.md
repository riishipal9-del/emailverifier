# Email Validator - Educational Tool

A comprehensive email validation tool with GUI and command-line interfaces. This tool demonstrates various email validation techniques for educational purposes.

## Features

- **Comprehensive Validation**: 
  - RFC 5322 compliant syntax validation
  - DNS MX record verification
  - Disposable email detection
  - Common typo suggestions

- **Multiple Interfaces**:
  - User-friendly GUI with tkinter
  - Command-line interface for automation
  - Bulk validation from files

- **Educational Focus**:
  - Clear validation explanations
  - Detailed error reporting
  - Validation technique demonstration

## Installation

### Requirements
- Python 3.7+
- dnspython
- tkinter (for GUI mode)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Default)
```bash
python main.py
```

### Command Line Mode
```bash
# Validate single email
python main.py -e user@example.com

# Validate emails from file
python main.py -f emails.txt

# Verbose output for bulk validation
python main.py -f emails.txt -v
```

### Building Executable
```bash
python build_exe.py
```

## Validation Features

### 1. Syntax Validation
- Checks RFC 5322 compliance
- Validates local and domain parts
- Detects common format errors

### 2. DNS Validation
- Verifies MX records exist
- Confirms domain accessibility
- Checks domain resolution

### 3. Typo Detection
- Suggests corrections for common mistakes
- Maps frequent typos to correct domains
- Helps users fix input errors

### 4. Disposable Email Detection
- Identifies temporary email services
- Educational awareness of disposable emails
- Helps understand email service types

## File Structure

```
emailverifier/
├── main.py              # Main entry point
├── email_validator.py   # Core validation logic
├── gui.py              # GUI interface
├── test_validator.py   # Test suite
├── build_exe.py        # Build script for executable
├── requirements.txt    # Python dependencies
├── test_emails.txt     # Sample email list
└── README.md          # This file
```

## Testing

Run the test suite:
```bash
python test_validator.py
```

## Educational Disclaimer

This tool is created for educational purposes to demonstrate email validation techniques. It should not be used for production email verification without additional considerations such as:

- Rate limiting for API calls
- Enhanced error handling
- Privacy and data protection compliance
- Commercial email verification service integration

## License

MIT License - See LICENSE file for details.
