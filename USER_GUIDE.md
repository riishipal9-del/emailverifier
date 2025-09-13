# Email Validator - Quick Start Guide

## Download and Run

1. Download the `EmailValidator` executable from the releases
2. Make it executable (Linux/Mac): `chmod +x EmailValidator`
3. Run the program

## Usage Modes

### 🖥️ GUI Mode (Recommended for beginners)
```bash
./EmailValidator
```
- User-friendly interface
- Single email validation
- Bulk validation from text input or files
- Real-time validation results
- Export results to file

### 💻 Command Line Mode (For automation)

**Single Email:**
```bash
./EmailValidator -e "user@example.com"
```

**Bulk Validation:**
```bash
./EmailValidator -f emails.txt
```

**Verbose Output:**
```bash
./EmailValidator -f emails.txt -v
```

## Sample Email File Format

Create a text file with one email per line:
```
user1@gmail.com
admin@company.org
test@invalid-domain.fake
contact@yahoo.com
```

## Understanding Results

### ✅ Valid Email
- Passes syntax validation
- Has valid MX records
- Not a disposable email service

### ❌ Invalid Email
Common issues:
- **Syntax errors**: Missing @, invalid characters
- **Domain issues**: No MX records, domain doesn't exist
- **Disposable emails**: Temporary email services

### 💡 Suggestions
The tool provides corrections for common typos:
- `gmial.com` → `gmail.com`
- `yahooo.com` → `yahoo.com`
- `hotmial.com` → `hotmail.com`

## Educational Purpose

This tool demonstrates:
- RFC-compliant email syntax validation
- DNS MX record verification
- Common email validation techniques
- Best practices for input validation

**Note**: For production use, consider additional factors like deliverability, reputation, and privacy compliance.