import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import time

# --- DATA STRUCTURES ---

class Node:
    """Linked List Node for Transactions"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class TransactionLinkedList:
    """Doubly Linked List to manage history in memory efficiently"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add_transaction(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('ibbl_final_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (acc_no TEXT PRIMARY KEY, pin TEXT, balance REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (acc_no TEXT, type TEXT, amount REAL, time TEXT)''')
    conn.commit()
    conn.close()

# --- ALGORITHMS ---

def binary_search_user(acc_list, target_acc):
    """Binary Search Algorithm: Complexity O(log n)"""
    low = 0
    high = len(acc_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if acc_list[mid][0] == target_acc:
            return acc_list[mid]
        elif acc_list[mid][0] < target_acc:
            low = mid + 1
        else:
            high = mid - 1
    return None

def quick_sort_descending(data):
    """Quick Sort: Sorts transactions by Amount (index 2) in Descending Order"""
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2][2]
    left = [x for x in data if x[2] > pivot]
    middle = [x for x in data if x[2] == pivot]
    right = [x for x in data if x[2] < pivot]
    return quick_sort_descending(left) + middle + quick_sort_descending(right)

# --- GUI CLASS ---
class AdvancedIslamicATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Islami Bank - ATM Terminal")
        self.root.geometry("500x750")
        self.root.configure(bg="#ffffff")
        self.current_user = None
        self.history_list = TransactionLinkedList()
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def draw_header(self, title):
        top = tk.Frame(self.root, bg="#006837", height=130)
        top.pack(fill="x")
        tk.Label(top, text="ISLAMI BANK", font=("Futura", 28, "bold"), fg="#ffffff", bg="#006837").pack(pady=(25,0))
        tk.Label(top, text=title, font=("Arial", 10, "italic"), fg="#a0d4b4", bg="#006837").pack()

    def main_menu(self):
        self.clear()
        self.draw_header("DUAL CURRENCY SMART TERMINAL")
        container = tk.Frame(self.root, bg="#ffffff")
        container.pack(pady=80)
        
        btn_style = {"font": ("Helvetica", 11, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        tk.Button(container, text="USER LOGIN", command=self.user_login, bg="#006837", fg="white", **btn_style).pack(pady=10)
        tk.Button(container, text="ADMIN ACCESS", command=self.admin_auth, bg="#1e293b", fg="white", **btn_style).pack(pady=10)
        
        tk.Label(self.root, text="Approved by Tanjim Ahamed Stamford", fg="#94a3b8", bg="#ffffff", font=("Arial", 8)).pack(side="bottom", pady=20)

    # --- ADMIN FUNCTIONS ---
    def admin_auth(self):
        pin = simpledialog.askstring("Admin", "Enter Security PIN:", show='*')
        if pin == "0000": self.admin_panel()
        elif pin: messagebox.showerror("Denied", "Incorrect Admin PIN")

    def admin_panel(self):
        self.clear()
        self.draw_header("ADMIN CONTROL PANEL")
        body = tk.Frame(self.root, bg="#ffffff")
        body.pack(pady=60)
        tk.Button(body, text="➕ Create New User", command=self.create_acc, bg="#006837", fg="white", width=25, height=2, bd=0).pack(pady=10)
        tk.Button(body, text="Back to Home", command=self.main_menu, bg="grey", fg="white", width=20, bd=0).pack(pady=20)

    def create_acc(self):
        acc = simpledialog.askstring("Input", "Account Number:")
        if not acc: return
        pin = simpledialog.askstring("Input", "Set 4-Digit PIN:")
        bal = simpledialog.askfloat("Input", "Initial Balance (BDT):")
        if acc and pin and bal is not None:
            conn = sqlite3.connect('ibbl_final_pro.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (acc, pin, bal))
                conn.commit()
                messagebox.showinfo("Success", f"Account {acc} Created!")
            except:
                messagebox.showerror("Error", "Account already exists!")
            conn.close()

    # --- USER LOGIN (Binary Search) ---
    def user_login(self):
        self.clear()
        self.draw_header("SECURE AUTHENTICATION")
        box = tk.Frame(self.root, bg="#f8fafc", padx=40, pady=40, highlightbackground="#e2e8f0", highlightthickness=1)
        box.pack(pady=60)
        
        tk.Label(box, text="Account Number", bg="#f8fafc", font=("Arial", 10)).pack(anchor="w")
        self.e_acc = tk.Entry(box, font=("Arial", 14), justify='center', bd=1); self.e_acc.pack(pady=(5,15))
        
        tk.Label(box, text="Secret PIN", bg="#f8fafc", font=("Arial", 10)).pack(anchor="w")
        self.e_pin = tk.Entry(box, font=("Arial", 14), show="*", justify='center', bd=1); self.e_pin.pack(pady=(5,25))
        
        tk.Button(box, text="LOG IN", command=self.auth_logic, bg="#006837", fg="white", width=20, height=2, bd=0).pack()
        tk.Button(self.root, text="← Back", command=self.main_menu, bd=0, bg="white", fg="grey").pack(pady=10)

    def auth_logic(self):
        conn = sqlite3.connect('ibbl_final_pro.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY acc_no ASC") # Binary Search requires sorted data
        acc_list = cursor.fetchall()
        conn.close()

        # Binary Search implementation
        user = binary_search_user(acc_list, self.e_acc.get())

        if user and user[1] == self.e_pin.get():
            self.current_user = list(user)
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Account or PIN!")

    # --- USER DASHBOARD ---
    def dashboard(self):
        self.clear()
        self.draw_header(f"ACCOUNT: {self.current_user[0]}")
        
        card = tk.Frame(self.root, bg="#006837", padx=20, pady=25)
        card.pack(pady=30, padx=50, fill="x")
        tk.Label(card, text="CURRENT BALANCE", fg="#a0d4b4", bg="#006837", font=("Arial", 9, "bold")).pack()
        self.lbl_bal = tk.Label(card, text=f"BDT {self.current_user[2]:,.2f}", fg="white", bg="#006837", font=("Arial", 26, "bold"))
        self.lbl_bal.pack(pady=10)

        grid = tk.Frame(self.root, bg="#ffffff")
        grid.pack()

        btn_style = {"bg": "#f1f5f9", "fg": "#1e293b", "width": 22, "height": 2, "font": ("Arial", 10, "bold"), "bd": 0, "cursor": "hand2"}
        
        tk.Button(grid, text="Withdraw Cash", command=lambda: self.perform_action("Withdraw"), **btn_style).pack(pady=5)
        tk.Button(grid, text="Deposit Cash", command=lambda: self.perform_action("Deposit"), **btn_style).pack(pady=5)
        tk.Button(grid, text="Mini Statement", command=self.view_history, **btn_style).pack(pady=5)
        tk.Button(grid, text="Logout", command=self.main_menu, bg="#fee2e2", fg="#ef4444", width=22, height=2, bd=0).pack(pady=20)

    def perform_action(self, mode):
        amt = simpledialog.askfloat(mode, f"Enter amount to {mode} (BDT):")
        if amt and amt > 0:
            if mode == "Withdraw" and amt > self.current_user[2]:
                messagebox.showerror("Error", "Insufficient Balance!")
                return
            
            conn = sqlite3.connect('ibbl_final_pro.db')
            cursor = conn.cursor()
            new_bal = self.current_user[2] - amt if mode == "Withdraw" else self.current_user[2] + amt
            ts = time.strftime('%H:%M:%S')
            
            cursor.execute("UPDATE users SET balance=? WHERE acc_no=?", (new_bal, self.current_user[0]))
            cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (self.current_user[0], mode, amt, ts))
            conn.commit(); conn.close()
            
            self.current_user[2] = new_bal
            self.lbl_bal.config(text=f"BDT {new_bal:,.2f}")
            messagebox.showinfo("Success", f"{mode} Successful!")

    # --- MINI STATEMENT (Quick Sort + Linked List) ---
    def view_history(self):
        conn = sqlite3.connect('ibbl_final_pro.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type, time, amount FROM history WHERE acc_no=?", (self.current_user[0],))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Info", "No history found.")
            return

        # 1. Algorithm: Quick Sort (Sorting by amount descending)
        sorted_rows = quick_sort_descending(list(rows))
        
        # 2. Data Structure: Doubly Linked List (Storing sorted data)
        self.history_list = TransactionLinkedList()
        for r in sorted_rows:
            self.history_list.add_transaction(r)

        # UI for Statement
        win = tk.Toplevel(self.root)
        win.title("Sorted Statement (By Amount)")
        win.geometry("450x450")
        
        tree = ttk.Treeview(win, columns=("T", "D", "A"), show='headings')
        tree.heading("T", text="Type"); tree.heading("D", text="Time"); tree.heading("A", text="Amount (BDT)")
        tree.pack(fill="both", expand=True)

        # 3. Traversal: Displaying from Linked List
        current = self.history_list.head
        while current:
            tree.insert("", "end", values=current.data)
            current = current.next

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AdvancedIslamicATM(root)
    root.mainloop()