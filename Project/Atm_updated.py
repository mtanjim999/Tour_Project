import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import time
import os

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('atm_pro_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts 
                      (acc_no TEXT PRIMARY KEY, pin TEXT, balance REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                      (acc_no TEXT, type TEXT, amount REAL, timestamp TEXT, receiver TEXT)''')
    conn.commit()
    conn.close()

# --- ALGORITHMS ---
def linear_search_account(acc_no):
    conn = sqlite3.connect('atm_pro_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    all_accs = cursor.fetchall()
    conn.close()
    for row in all_accs:
        if row[0] == acc_no: return row
    return None

def quick_sort_transactions(data):
    """Advanced Quick Sort: Amount onujayi sorting"""
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2][2] # Amount is at index 2
    left = [x for x in data if x[2] > pivot]
    middle = [x for x in data if x[2] == pivot]
    right = [x for x in data if x[2] < pivot]
    return quick_sort_transactions(left) + middle + quick_sort_transactions(right)

# --- MAIN APP ---
class ProfessionalATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Elite Bank Pro v2.0")
        self.root.geometry("500x700")
        self.root.configure(bg="#0f172a") # Modern Dark Blue
        self.current_user = None
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="🏦 ELITE BANK PRO", font=("Impact", 30), fg="#38bdf8", bg="#0f172a").pack(pady=60)
        
        btn_style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        tk.Button(self.root, text="USER LOGIN", command=self.user_login, bg="#38bdf8", fg="black", **btn_style).pack(pady=10)
        tk.Button(self.root, text="ADMIN PANEL", command=self.admin_access, bg="#1e293b", fg="white", **btn_style).pack(pady=10)
        tk.Button(self.root, text="EXIT", command=self.root.quit, bg="#ef4444", fg="white", font=("Arial", 10)).pack(pady=40)

    # --- ADMIN LOGIC ---
    def admin_access(self):
        pin = simpledialog.askstring("Security", "Enter Admin Security Key:", show='*')
        if pin == "0000":
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Unauthorized!")

    def admin_panel(self):
        self.clear()
        tk.Label(self.root, text="ADMIN CONTROL", font=("Arial", 18, "bold"), fg="white", bg="#0f172a").pack(pady=30)
        
        tk.Button(self.root, text="Create New Account", command=self.create_account, width=25, bg="#334155", fg="white").pack(pady=10)
        tk.Button(self.root, text="Logout Admin", command=self.main_menu, bg="#ef4444", fg="white").pack(pady=20)

    def create_account(self):
        acc = simpledialog.askstring("Input", "Set Account Number:")
        if not acc or linear_search_account(acc):
            messagebox.showerror("Error", "Invalid or Duplicate Account!")
            return
        pin = simpledialog.askstring("Input", "Set 4-Digit PIN:")
        bal = simpledialog.askfloat("Input", "Initial Balance:")
        
        if acc and pin and bal is not None:
            conn = sqlite3.connect('atm_pro_database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)", (acc, pin, bal))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Account {acc} created!")

    # --- USER LOGIC ---
    def user_login(self):
        self.clear()
        tk.Label(self.root, text="SECURE TERMINAL", font=("Arial", 16), fg="#38bdf8", bg="#0f172a").pack(pady=40)
        
        tk.Label(self.root, text="Account Number", fg="white", bg="#0f172a").pack()
        self.e_acc = tk.Entry(self.root, font=("Arial", 14), justify="center"); self.e_acc.pack(pady=5)
        
        tk.Label(self.root, text="Secret PIN", fg="white", bg="#0f172a").pack()
        self.e_pin = tk.Entry(self.root, font=("Arial", 14), show="*", justify="center"); self.e_pin.pack(pady=5)

        tk.Button(self.root, text="AUTHENTICATE", command=self.auth, bg="#38bdf8", width=20, height=2).pack(pady=30)
        tk.Button(self.root, text="BACK", command=self.main_menu, bg="#ef4444", fg="white").pack()

    def auth(self):
        user = linear_search_account(self.e_acc.get())
        if user and user[1] == self.e_pin.get():
            self.current_user = list(user)
            self.dashboard()
        else:
            messagebox.showerror("Denied", "Identity Verification Failed!")

    def dashboard(self):
        self.clear()
        header = tk.Frame(self.root, bg="#1e293b", height=60); header.pack(fill="x")
        tk.Label(header, text=f"ACC: {self.current_user[0]}", fg="white", bg="#1e293b").pack(side="left", padx=20)
        
        self.lbl_bal = tk.Label(self.root, text=f"${self.current_user[2]:,.2f}", font=("Arial", 40, "bold"), fg="#10b981", bg="#0f172a")
        self.lbl_bal.pack(pady=60)

        grid = tk.Frame(self.root, bg="#0f172a")
        grid.pack()

        # Dashboard Buttons
        ops = [("Withdraw", lambda: self.transact("Withdraw")), 
               ("Deposit", lambda: self.transact("Deposit")),
               ("Fund Transfer", self.transfer_money),
               ("Statement", self.view_history),
               ("Logout", self.main_menu)]

        for txt, cmd in ops:
            color = "#334155" if txt != "Logout" else "#ef4444"
            tk.Button(grid, text=txt, command=cmd, width=20, height=2, bg=color, fg="white", bd=0).pack(pady=5)

    def transact(self, mode):
        amt = simpledialog.askfloat(mode, f"Enter amount to {mode}:")
        if amt and amt > 0:
            if mode == "Withdraw" and amt > self.current_user[2]:
                messagebox.showerror("Error", "Insufficient Funds!")
                return
            self.execute_db_update(amt, mode)

    def transfer_money(self):
        target = simpledialog.askstring("Transfer", "Enter Receiver Account Number:")
        if target == self.current_user[0]:
            messagebox.showwarning("Error", "Cannot transfer to self!")
            return
        
        receiver = linear_search_account(target)
        if receiver:
            amt = simpledialog.askfloat("Transfer", f"Sending to {target}\nEnter Amount:")
            if amt and amt <= self.current_user[2]:
                # Update Sender
                self.execute_db_update(amt, "Transfer", target)
                # Update Receiver
                conn = sqlite3.connect('atm_pro_database.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no = ?", (amt, target))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Successfully transferred ${amt} to {target}")
            else:
                messagebox.showerror("Error", "Insufficient Balance!")
        else:
            messagebox.showerror("Not Found", "Receiver Account not found!")

    def execute_db_update(self, amount, type, receiver="N/A"):
        conn = sqlite3.connect('atm_pro_database.db')
        cursor = conn.cursor()
        new_bal = self.current_user[2] - amount if type in ["Withdraw", "Transfer"] else self.current_user[2] + amount
        
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?", (new_bal, self.current_user[0]))
        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", (self.current_user[0], type, amount, ts, receiver))
        conn.commit()
        conn.close()
        
        self.current_user[2] = new_bal
        self.lbl_bal.config(text=f"${new_bal:,.2f}")
        self.generate_receipt(type, amount, receiver)

    def generate_receipt(self, type, amount, receiver):
        receipt_text = f"--- ELITE BANK RECEIPT ---\nDate: {time.ctime()}\nType: {type}\nAmount: ${amount}\nReceiver: {receiver}\nBalance: ${self.current_user[2]}\n--------------------------"
        with open("last_receipt.txt", "w") as f:
            f.write(receipt_text)
        messagebox.showinfo("Receipt", "Transaction successful! Receipt saved to last_receipt.txt")

    def view_history(self):
        conn = sqlite3.connect('atm_pro_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type, timestamp, amount, receiver FROM transactions WHERE acc_no = ?", (self.current_user[0],))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Info", "No history found.")
            return

        sorted_data = quick_sort_transactions(list(rows)) # Using Quick Sort

        win = tk.Toplevel(self.root)
        win.title("Account Statement (Sorted by Amount)")
        win.geometry("500x400")
        
        tree = ttk.Treeview(win, columns=('Type', 'Time', 'Amount', 'Receiver'), show='headings')
        for c in ('Type', 'Time', 'Amount', 'Receiver'): tree.heading(c, text=c)
        tree.pack(expand=True, fill='both')

        for r in sorted_data:
            tree.insert("", "end", values=r)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ProfessionalATM(root)
    root.mainloop()