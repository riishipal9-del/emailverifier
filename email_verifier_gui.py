import tkinter as tk
from tkinter import ttk, messagebox
import re
import dns.resolver
import socket
import threading

class EmailVerifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Verifier")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # Icon not found, continue without it
            
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Email Address Verifier", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Verify Email", padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Email input
        email_frame = ttk.Frame(input_frame)
        email_frame.pack(fill=tk.X, pady=5)
        
        email_label = ttk.Label(email_frame, text="Email Address:", width=15)
        email_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(email_frame, textvariable=self.email_var, width=40)
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Verify button
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.verify_button = ttk.Button(button_frame, text="Verify", command=self.start_verification)
        self.verify_button.pack(padx=5)
        
        # Progress indicator
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode="indeterminate")
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results display (using Text widget with scrollbar)
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=10)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
    def start_verification(self):
        """Start verification in a separate thread"""
        email = self.email_var.get().strip()
        if not email:
            messagebox.showwarning("Input Error", "Please enter an email address")
            return
            
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.progress_var.set("Verifying...")
        self.progress_bar.pack(fill=tk.X, padx=20, pady=5)
        self.progress_bar.start(10)
        self.verify_button.config(state=tk.DISABLED)
        
        # Start verification in a separate thread
        thread = threading.Thread(target=self.verify_email, args=(email,))
        thread.daemon = True
        thread.start()
        
    def verify_email(self, email):
        """Verify the email address"""
        try:
            # Step 1: Syntax check
            self.update_result("1. Checking email syntax...")
            syntax_valid = self.check_syntax(email)
            
            if not syntax_valid:
                self.update_result("   ❌ Invalid email syntax")
                return
            self.update_result("   ✅ Syntax is valid")
            
            # Step 2: Domain validation
            self.update_result("\n2. Checking domain...")
            domain = email.split('@')[1]
            domain_valid = self.check_domain(domain)
            
            if not domain_valid:
                self.update_result(f"   ❌ Domain '{domain}' does not exist or cannot be reached")
                return
            self.update_result(f"   ✅ Domain '{domain}' exists")
            
            # Step 3: Check MX records
            self.update_result("\n3. Checking mail server records...")
            mx_records = self.check_mx_records(domain)
            
            if not mx_records:
                self.update_result(f"   ❌ No mail servers found for '{domain}'")
                return
            self.update_result(f"   ✅ Mail servers found: {', '.join(mx_records)}")
            
            self.update_result("\n✅ Email address appears to be valid!")
            
        except Exception as e:
            self.update_result(f"\n❌ Error during verification: {str(e)}")
        finally:
            # Re-enable UI elements
            self.root.after(0, self.finalize_verification)
    
    def finalize_verification(self):
        """Re-enable UI elements after verification completes"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_var.set("Verification complete")
        self.verify_button.config(state=tk.NORMAL)
    
    def update_result(self, message):
        """Update the results text widget safely from a thread"""
        self.root.after(0, lambda: self._update_result_text(message))
    
    def _update_result_text(self, message):
        """Update the results text widget (called from main thread)"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
    
    def check_syntax(self, email):
        """Check if email syntax is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def check_domain(self, domain):
        """Check if domain exists"""
        try:
            socket.gethostbyname(domain)
            return True
        except:
            return False
    
    def check_mx_records(self, domain):
        """Check if MX records exist for the domain"""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return [str(mx.exchange)[:-1] for mx in mx_records]
        except:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailVerifierGUI(root)
    root.mainloop()