"""
Email Validator GUI - User-friendly interface for email validation
For Educational Purposes Only

This module provides a tkinter-based GUI for the email validator.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
from typing import List
from email_validator import EmailValidator, ValidationResult


class EmailValidatorGUI:
    """GUI application for email validation"""
    
    def __init__(self):
        self.validator = EmailValidator()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components"""
        self.root = tk.Tk()
        self.root.title("Email Validator - Educational Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Email Validator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Single email validation section
        single_frame = ttk.LabelFrame(main_frame, text="Single Email Validation", 
                                     padding="10")
        single_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                         pady=(0, 10))
        single_frame.columnconfigure(1, weight=1)
        
        ttk.Label(single_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.email_entry = ttk.Entry(single_frame, width=40)
        self.email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.email_entry.bind('<Return>', self.validate_single_email)
        
        self.validate_btn = ttk.Button(single_frame, text="Validate", 
                                      command=self.validate_single_email)
        self.validate_btn.grid(row=0, column=2)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Validation Results", 
                                      padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, width=80, height=15,
                                                     wrap=tk.WORD, font=('Consolas', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bulk validation section
        bulk_frame = ttk.LabelFrame(main_frame, text="Bulk Email Validation", 
                                   padding="10")
        bulk_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                       pady=(0, 10))
        bulk_frame.columnconfigure(1, weight=1)
        
        ttk.Label(bulk_frame, text="Emails (one per line):").grid(row=0, column=0, 
                                                                  sticky=(tk.W, tk.N), padx=(0, 5))
        
        self.bulk_text = tk.Text(bulk_frame, width=50, height=5, wrap=tk.WORD,
                                font=('Consolas', 9))
        self.bulk_text.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        bulk_btn_frame = ttk.Frame(bulk_frame)
        bulk_btn_frame.grid(row=0, column=2, sticky=(tk.N))
        
        self.bulk_validate_btn = ttk.Button(bulk_btn_frame, text="Validate All", 
                                           command=self.validate_bulk_emails)
        self.bulk_validate_btn.pack(pady=(0, 5))
        
        ttk.Button(bulk_btn_frame, text="Load from File", 
                  command=self.load_from_file).pack(pady=(0, 5))
        
        ttk.Button(bulk_btn_frame, text="Save Results", 
                  command=self.save_results).pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        # Educational info
        info_frame = ttk.LabelFrame(main_frame, text="Educational Information", 
                                   padding="5")
        info_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        info_text = ("This tool demonstrates email validation techniques:\n"
                    "• Syntax validation using RFC-compliant regex\n"
                    "• DNS MX record verification\n"
                    "• Common typo detection and suggestions\n"
                    "• Disposable email service detection")
        
        ttk.Label(info_frame, text=info_text, font=('Arial', 8)).pack(anchor=tk.W)
    
    def update_status(self, message: str):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def display_result(self, result: ValidationResult, clear_previous: bool = True):
        """Display validation result in the text area"""
        if clear_previous:
            self.results_text.delete(1.0, tk.END)
        
        # Format result
        output = f"Email: {result.email}\n"
        output += f"Status: {'✓ VALID' if result.is_valid else '✗ INVALID'}\n"
        output += "=" * 50 + "\n\n"
        
        # Validation details
        output += "Validation Details:\n"
        for check, passed in result.validation_details.items():
            status = "✓" if passed else "✗"
            output += f"  {status} {check.replace('_', ' ').title()}\n"
        
        # Issues
        if result.issues:
            output += "\nIssues Found:\n"
            for issue in result.issues:
                output += f"  • {issue}\n"
        
        # Suggestions
        if result.suggestions:
            output += "\nSuggestions:\n"
            for suggestion in result.suggestions:
                output += f"  • {suggestion}\n"
        
        output += "\n" + "=" * 60 + "\n\n"
        
        self.results_text.insert(tk.END, output)
        self.results_text.see(tk.END)
    
    def validate_single_email(self, event=None):
        """Validate a single email address"""
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address")
            return
        
        self.update_status("Validating email...")
        self.progress.start()
        
        # Run validation in separate thread to prevent GUI freezing
        def validate_thread():
            try:
                result = self.validator.validate_email(email)
                self.root.after(0, lambda: self.finish_single_validation(result))
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(str(e)))
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def finish_single_validation(self, result: ValidationResult):
        """Finish single email validation"""
        self.progress.stop()
        self.display_result(result)
        self.update_status(f"Validation complete - {'Valid' if result.is_valid else 'Invalid'}")
    
    def validate_bulk_emails(self):
        """Validate multiple email addresses"""
        emails_text = self.bulk_text.get(1.0, tk.END).strip()
        if not emails_text:
            messagebox.showwarning("Warning", "Please enter email addresses")
            return
        
        emails = [email.strip() for email in emails_text.split('\n') if email.strip()]
        if not emails:
            messagebox.showwarning("Warning", "No valid email addresses found")
            return
        
        self.update_status(f"Validating {len(emails)} emails...")
        self.progress.start()
        self.bulk_validate_btn.config(state='disabled')
        
        def validate_bulk_thread():
            try:
                results = self.validator.validate_bulk(emails)
                self.root.after(0, lambda: self.finish_bulk_validation(results))
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(str(e)))
        
        threading.Thread(target=validate_bulk_thread, daemon=True).start()
    
    def finish_bulk_validation(self, results: List[ValidationResult]):
        """Finish bulk email validation"""
        self.progress.stop()
        self.bulk_validate_btn.config(state='normal')
        
        # Display summary
        valid_count = sum(1 for r in results if r.is_valid)
        self.results_text.delete(1.0, tk.END)
        
        summary = f"BULK VALIDATION SUMMARY\n"
        summary += f"Total emails: {len(results)}\n"
        summary += f"Valid emails: {valid_count}\n"
        summary += f"Invalid emails: {len(results) - valid_count}\n"
        summary += "=" * 60 + "\n\n"
        
        self.results_text.insert(tk.END, summary)
        
        # Display individual results
        for i, result in enumerate(results, 1):
            self.display_result(result, clear_previous=False)
        
        self.update_status(f"Bulk validation complete - {valid_count}/{len(results)} valid")
    
    def load_from_file(self):
        """Load emails from a file"""
        filename = filedialog.askopenfilename(
            title="Select email file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.bulk_text.delete(1.0, tk.END)
                self.bulk_text.insert(1.0, content)
                self.update_status(f"Loaded emails from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_results(self):
        """Save validation results to a file"""
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def handle_error(self, error_msg: str):
        """Handle validation errors"""
        self.progress.stop()
        self.bulk_validate_btn.config(state='normal')
        messagebox.showerror("Error", f"Validation failed: {error_msg}")
        self.update_status("Error occurred during validation")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = EmailValidatorGUI()
    app.run()