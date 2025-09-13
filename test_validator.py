"""
Test Suite for Email Validator
For Educational Purposes Only
"""

import unittest
from email_validator import EmailValidator, ValidationResult


class TestEmailValidator(unittest.TestCase):
    """Test cases for EmailValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = EmailValidator()
    
    def test_valid_emails(self):
        """Test validation of valid email addresses"""
        valid_emails = [
            "test@gmail.com",
            "user.name@example.com",
            "admin@example.org",
            "contact123@company.co.uk"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                result = self.validator.validate_email(email)
                self.assertTrue(result.validation_details['syntax_valid'], 
                              f"Syntax should be valid for {email}")
    
    def test_invalid_syntax(self):
        """Test validation of emails with invalid syntax"""
        invalid_emails = [
            "notanemail",           # Missing @
            "user@@example.com",    # Double @
            "@example.com",         # Missing local part
            "user@",                # Missing domain
            "user@domain",          # Missing TLD
            ".user@example.com",    # Starts with dot
            "user.@example.com",    # Ends with dot
            "user..name@example.com" # Consecutive dots
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                result = self.validator.validate_email(email)
                self.assertFalse(result.validation_details['syntax_valid'],
                               f"Syntax should be invalid for {email}")
    
    def test_typo_suggestions(self):
        """Test typo detection and suggestions"""
        typos = {
            "test@gmial.com": "gmail.com",
            "user@yahooo.com": "yahoo.com",
            "admin@hotmial.com": "hotmail.com"
        }
        
        for email, expected_domain in typos.items():
            with self.subTest(email=email):
                suggestions = self.validator.suggest_corrections(email)
                self.assertTrue(any(expected_domain in suggestion for suggestion in suggestions),
                              f"Should suggest correction for {email}")
    
    def test_disposable_detection(self):
        """Test disposable email detection"""
        disposable_emails = [
            "test@10minutemail.com",
            "user@tempmail.org",
            "admin@guerrillamail.com"
        ]
        
        for email in disposable_emails:
            with self.subTest(email=email):
                is_disposable = self.validator.check_disposable(email)
                self.assertTrue(is_disposable, f"{email} should be detected as disposable")
    
    def test_bulk_validation(self):
        """Test bulk email validation"""
        emails = [
            "valid@gmail.com",
            "invalid.email",
            "another@yahoo.com"
        ]
        
        results = self.validator.validate_bulk(emails)
        self.assertEqual(len(results), len(emails))
        
        # Check that all results are ValidationResult instances
        for result in results:
            self.assertIsInstance(result, ValidationResult)
    
    def test_empty_email(self):
        """Test handling of empty email"""
        result = self.validator.validate_email("")
        self.assertFalse(result.is_valid)
        self.assertIn("Email cannot be empty", str(result.issues))
    
    def test_validation_result_structure(self):
        """Test ValidationResult structure"""
        result = self.validator.validate_email("test@example.com")
        
        # Check required attributes
        self.assertTrue(hasattr(result, 'is_valid'))
        self.assertTrue(hasattr(result, 'email'))
        self.assertTrue(hasattr(result, 'issues'))
        self.assertTrue(hasattr(result, 'suggestions'))
        self.assertTrue(hasattr(result, 'validation_details'))
        
        # Check types
        self.assertIsInstance(result.is_valid, bool)
        self.assertIsInstance(result.email, str)
        self.assertIsInstance(result.issues, list)
        self.assertIsInstance(result.suggestions, list)
        self.assertIsInstance(result.validation_details, dict)


if __name__ == '__main__':
    unittest.main()