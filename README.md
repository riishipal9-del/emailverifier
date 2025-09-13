# Email Verifier GUI

A graphical user interface (GUI) application for verifying email addresses.

## Overview

This application helps validate email addresses through multiple verification steps:

1. **Syntax Verification**: Checks if the email follows the correct format.
2. **Domain Verification**: Verifies that the domain exists.
3. **Mail Server Verification**: Confirms the domain has mail servers (MX records).

## Features

- Clean and intuitive graphical interface
- Multi-threaded verification (UI remains responsive during checks)
- Detailed verification steps with visual indicators
- Comprehensive results display

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/riishipal9-del/email-verifier.git
   cd email-verifier
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python email_verifier_gui.py
   ```

2. Enter an email address in the input field.

3. Click the "Verify" button to start the verification process.

4. View the detailed results in the results section.

## Screenshots

![Application Screenshot](screenshot.png)
*(Add a screenshot of your application here)*

## Limitations

- The application doesn't perform an actual email delivery test
- Some corporate email servers might block DNS lookups
- Network issues can affect verification results

## License

MIT License

## Author

[riishipal9-del](https://github.com/riishipal9-del)