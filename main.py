#!/usr/bin/env python3
"""
Email Validator Main Entry Point
For Educational Purposes Only

A comprehensive email validation tool with GUI interface.
"""

import sys
import argparse
from email_validator import EmailValidator

# Try to import GUI, handle gracefully if not available
try:
    from gui import EmailValidatorGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def command_line_mode(args):
    """Run validation in command line mode"""
    validator = EmailValidator()
    
    if args.email:
        # Single email validation
        result = validator.validate_email(args.email)
        print(f"Email: {result.email}")
        print(f"Valid: {result.is_valid}")
        
        if result.issues:
            print("\nIssues:")
            for issue in result.issues:
                print(f"  - {issue}")
        
        if result.suggestions:
            print("\nSuggestions:")
            for suggestion in result.suggestions:
                print(f"  - {suggestion}")
        
        print("\nValidation Details:")
        for check, passed in result.validation_details.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check.replace('_', ' ').title()}")
    
    elif args.file:
        # Bulk validation from file
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                emails = [line.strip() for line in f if line.strip()]
            
            results = validator.validate_bulk(emails)
            valid_count = sum(1 for r in results if r.is_valid)
            
            print(f"Validation Summary:")
            print(f"Total emails: {len(results)}")
            print(f"Valid emails: {valid_count}")
            print(f"Invalid emails: {len(results) - valid_count}")
            
            if args.verbose:
                print("\nDetailed Results:")
                for result in results:
                    print(f"\n{result.email}: {'VALID' if result.is_valid else 'INVALID'}")
                    if result.issues:
                        for issue in result.issues:
                            print(f"  - {issue}")
        
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Email Validator - Educational Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Launch GUI mode
  python main.py -e user@example.com       # Validate single email
  python main.py -f emails.txt             # Validate emails from file
  python main.py -f emails.txt -v          # Verbose output
        """
    )
    
    parser.add_argument('-e', '--email', 
                       help='Single email address to validate')
    parser.add_argument('-f', '--file', 
                       help='File containing email addresses (one per line)')
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Verbose output for bulk validation')
    parser.add_argument('--gui', 
                       action='store_true',
                       help='Force GUI mode (default if no other options)')
    
    args = parser.parse_args()
    
    # Determine mode
    if args.email or args.file:
        # Command line mode
        command_line_mode(args)
    else:
        # GUI mode (default)
        if not GUI_AVAILABLE:
            print("GUI mode is not available (tkinter not installed)")
            print("Use command line options instead:")
            print("  python main.py -e user@example.com")
            print("  python main.py -f emails.txt")
            sys.exit(1)
        
        try:
            app = EmailValidatorGUI()
            app.run()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()