"""
Email Validator - Comprehensive Email Validation Module
For Educational Purposes Only

This module provides accurate email validation using multiple validation techniques:
1. Syntax validation using regex patterns
2. Domain validation 
3. DNS MX record checking
4. Common typo detection
"""

import re
import socket
import dns.resolver
from typing import Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Container for email validation results"""
    is_valid: bool
    email: str
    issues: List[str]
    suggestions: List[str]
    validation_details: Dict[str, bool]


class EmailValidator:
    """Comprehensive email validator with educational explanations"""
    
    def __init__(self):
        # RFC 5322 compliant regex pattern
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        # Common domain typos mapping
        self.domain_corrections = {
            'gmial.com': 'gmail.com',
            'gmai.com': 'gmail.com',
            'yahooo.com': 'yahoo.com',
            'hotmial.com': 'hotmail.com',
            'outlok.com': 'outlook.com',
            'iclod.com': 'icloud.com',
        }
        
        # Disposable email domains (educational awareness)
        self.disposable_domains = {
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email'
        }
    
    def validate_syntax(self, email: str) -> Tuple[bool, List[str]]:
        """Validate email syntax using RFC compliant regex"""
        issues = []
        
        if not email or not isinstance(email, str):
            issues.append("Email cannot be empty or non-string")
            return False, issues
        
        email = email.strip()
        
        # Check basic format
        if '@' not in email:
            issues.append("Missing @ symbol")
            return False, issues
        
        if email.count('@') != 1:
            issues.append("Multiple @ symbols found")
            return False, issues
        
        local, domain = email.split('@', 1)
        
        # Validate local part
        if not local:
            issues.append("Missing local part (before @)")
        elif len(local) > 64:
            issues.append("Local part too long (max 64 characters)")
        elif local.startswith('.') or local.endswith('.'):
            issues.append("Local part cannot start or end with dot")
        elif '..' in local:
            issues.append("Consecutive dots not allowed in local part")
        
        # Validate domain part
        if not domain:
            issues.append("Missing domain part (after @)")
        elif len(domain) > 253:
            issues.append("Domain too long (max 253 characters)")
        elif not re.match(r'^[a-zA-Z0-9.-]+$', domain):
            issues.append("Domain contains invalid characters")
        elif domain.startswith('.') or domain.endswith('.'):
            issues.append("Domain cannot start or end with dot")
        elif '..' in domain:
            issues.append("Consecutive dots not allowed in domain")
        elif '.' not in domain:
            issues.append("Domain must contain at least one dot")
        
        # Final regex check
        if not issues and not self.email_pattern.match(email):
            issues.append("Email format doesn't match RFC standards")
        
        return len(issues) == 0, issues
    
    def check_domain_mx(self, domain: str) -> Tuple[bool, List[str]]:
        """Check if domain has valid MX records"""
        issues = []
        
        try:
            # Check MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                issues.append("No MX records found for domain")
                return False, issues
            
            return True, []
        
        except dns.resolver.NXDOMAIN:
            issues.append("Domain does not exist")
        except dns.resolver.NoAnswer:
            issues.append("No MX records found for domain")
        except Exception as e:
            issues.append(f"DNS lookup failed: {str(e)}")
        
        return False, issues
    
    def suggest_corrections(self, email: str) -> List[str]:
        """Suggest corrections for common typos"""
        suggestions = []
        
        if '@' in email:
            local, domain = email.split('@', 1)
            
            # Check for domain corrections
            if domain.lower() in self.domain_corrections:
                corrected = f"{local}@{self.domain_corrections[domain.lower()]}"
                suggestions.append(f"Did you mean: {corrected}?")
        
        return suggestions
    
    def check_disposable(self, email: str) -> bool:
        """Check if email uses a disposable email service"""
        if '@' in email:
            domain = email.split('@', 1)[1].lower()
            return domain in self.disposable_domains
        return False
    
    def validate_email(self, email: str) -> ValidationResult:
        """Comprehensive email validation with detailed results"""
        validation_details = {}
        all_issues = []
        suggestions = []
        
        # 1. Syntax validation
        syntax_valid, syntax_issues = self.validate_syntax(email)
        validation_details['syntax_valid'] = syntax_valid
        all_issues.extend(syntax_issues)
        
        if not syntax_valid:
            return ValidationResult(
                is_valid=False,
                email=email,
                issues=all_issues,
                suggestions=self.suggest_corrections(email),
                validation_details=validation_details
            )
        
        # 2. Domain MX record validation
        domain = email.split('@', 1)[1]
        mx_valid, mx_issues = self.check_domain_mx(domain)
        validation_details['mx_records_valid'] = mx_valid
        all_issues.extend(mx_issues)
        
        # 3. Disposable email check
        is_disposable = self.check_disposable(email)
        validation_details['is_disposable'] = is_disposable
        if is_disposable:
            all_issues.append("Email uses a disposable email service")
        
        # 4. Get suggestions
        suggestions = self.suggest_corrections(email)
        
        # Determine overall validity
        is_valid = syntax_valid and mx_valid and not is_disposable
        
        return ValidationResult(
            is_valid=is_valid,
            email=email,
            issues=all_issues,
            suggestions=suggestions,
            validation_details=validation_details
        )
    
    def validate_bulk(self, emails: List[str]) -> List[ValidationResult]:
        """Validate multiple emails"""
        return [self.validate_email(email) for email in emails]