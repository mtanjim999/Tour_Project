import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import uuid

# ================= DATABASE =================
conn = sqlite3.connect("atm.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    pin TEXT,
    balance INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    name TEXT,
    type TEXT,
    amount INTEGER,
    session_id TEXT
)
""")

conn.commit()

# ================= QUEUE =================
class ATMQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

atm = ATMQueue()

# ================= UI =================
root = tk.Tk() #main window
root.title("ATM System Pro")
root.geometry("520x600")

tk.Label(root, text="ATM Queue System", font=("Arial", 16, "bold")).pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

# ================= ANIMATION =================
def animate(text):
    for i in range(3):
        status_label.config(text=text + "." * (i+1))
        root.update()
        time.sleep(0.2)
    status_label.config(text=text + " Done!")

# ================= INPUT HELP =================
def clear(entry, txt):
    if entry.get() == txt:
        entry.delete(0, tk.END)

def reset_fields():
    name_entry.delete(0, tk.END)
    pin_entry.delete(0, tk.END)
    balance_entry.delete(0, tk.END)

# ================= INPUT FIELDS =================
name_entry = tk.Entry(root)
name_entry.insert(0, "Enter Name")
name_entry.pack(pady=5)
name_entry.bind("<FocusIn>", lambda e: clear(name_entry, "Enter Name"))

pin_entry = tk.Entry(root)
pin_entry.insert(0, "Enter PIN")
pin_entry.pack(pady=5)
pin_entry.bind("<FocusIn>", lambda e: clear(pin_entry, "Enter PIN"))

balance_entry = tk.Entry(root)
balance_entry.insert(0, "Initial Balance")
balance_entry.pack(pady=5)
balance_entry.bind("<FocusIn>", lambda e: clear(balance_entry, "Initial Balance"))

queue_box = tk.Listbox(root, width=55)
queue_box.pack(pady=10)

# ================= ENTER FLOW =================
name_entry.bind("<Return>", lambda e: pin_entry.focus())
pin_entry.bind("<Return>", lambda e: balance_entry.focus())
balance_entry.bind("<Return>", lambda e: add_user())

# ================= QUEUE UPDATE =================
def update_queue():
    queue_box.delete(0, tk.END)
    for i, item in enumerate(atm.queue):
        queue_box.insert(tk.END, f"{i+1}. {item['name']}")

# ================= ADD USER =================
def add_user():
    name = name_entry.get().strip()
    pin = pin_entry.get().strip()
    balance = balance_entry.get().strip()

    if name == "" or pin == "":
        messagebox.showerror("Error", "Name & PIN required!")
        return

    session_id = str(uuid.uuid4())

    cursor.execute("SELECT * FROM users WHERE name=?", (name,))
    data = cursor.fetchone()

    if data:
        if data[1] != pin:
            messagebox.showerror("Error", "Wrong PIN!")
            return

        atm.enqueue({"name": name, "session": session_id})
        status_label.config(text=f"{name} joined queue")

    else:
        if not balance.isdigit():
            messagebox.showerror("Error", "Enter valid balance!")
            return

        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (name, pin, int(balance)))
        conn.commit()

        atm.enqueue({"name": name, "session": session_id})
        status_label.config(text=f"{name} created & added")

    update_queue()
    reset_fields()

# ================= SERVE USER =================
def serve_user():
    if atm.is_empty():
        messagebox.showinfo("Info", "Queue empty!")
        return

    item = atm.dequeue()
    update_queue()

    name = item["name"]
    session_id = item["session"]

    pin_win = tk.Toplevel(root)
    pin_win.title("PIN Verify")
    pin_win.geometry("300x200")

    tk.Label(pin_win, text=f"{name} Enter PIN").pack(pady=10)

    pin_input = tk.Entry(pin_win, show="*")
    pin_input.pack(pady=5)

    def verify():
        pin = pin_input.get()

        cursor.execute("SELECT * FROM users WHERE name=? AND pin=?", (name, pin))
        if cursor.fetchone():
            pin_win.destroy()
            open_atm(name, session_id)
        else:
            messagebox.showerror("Error", "Wrong PIN!")

    tk.Button(pin_win, text="Login", command=verify).pack(pady=10)

# ================= ATM WINDOW =================
def open_atm(username, session_id):
    atm_win = tk.Toplevel(root)
    atm_win.title(username)
    atm_win.geometry("350x400")

    tk.Label(atm_win, text=f"Welcome {username}", font=("Arial", 12, "bold")).pack(pady=5)

    amount_entry = tk.Entry(atm_win)
    amount_entry.pack(pady=5)

    # ---------- DEPOSIT ----------
    def deposit():
        amount = amount_entry.get().strip()
        if not amount.isdigit():
            messagebox.showerror("Error", "Invalid amount!")
            return

        animate("Depositing")

        cursor.execute("UPDATE users SET balance = balance + ? WHERE name=?",
                       (int(amount), username))

        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)",
                       (username, "Deposit", int(amount), session_id))

        conn.commit()
        amount_entry.delete(0, tk.END)

    # ---------- WITHDRAW ----------
    def withdraw():
        amount = amount_entry.get().strip()
        if not amount.isdigit():
            messagebox.showerror("Error", "Invalid amount!")
            return

        cursor.execute("SELECT balance FROM users WHERE name=?", (username,))
        bal = cursor.fetchone()[0]

        if int(amount) > bal:
            messagebox.showerror("Error", "Insufficient Balance!")
            return

        animate("Withdrawing")

        cursor.execute("UPDATE users SET balance = balance - ? WHERE name=?",
                       (int(amount), username))

        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)",
                       (username, "Withdraw", int(amount), session_id))

        conn.commit()
        amount_entry.delete(0, tk.END)

    # ---------- CHECK BALANCE ----------
    def check_balance():
        win = tk.Toplevel(atm_win)
        win.title("Balance")
        win.geometry("300x300")

        cursor.execute("SELECT balance FROM users WHERE name=?", (username,))
        bal = cursor.fetchone()[0]

        tk.Label(win, text=f"Balance: {bal}", font=("Arial", 12, "bold")).pack(pady=10)

        def show_history():
            hist = tk.Toplevel(win)
            hist.title("Transaction History")
            hist.geometry("300x300")

            frame = tk.Frame(hist)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=listbox.yview)

            cursor.execute("""
                SELECT type, amount FROM transactions
                WHERE session_id=?
            """, (session_id,))

            data = cursor.fetchall()

            if not data:
                listbox.insert(tk.END, "No transactions")
            else:
                for t in data:
                    listbox.insert(tk.END, f"{t[0]} : {t[1]}")

        tk.Button(win, text="Show Transactions", command=show_history).pack(pady=20)

    # ================= BUTTONS =================
    tk.Button(atm_win, text="Deposit", command=deposit, width=20).pack(pady=5)
    tk.Button(atm_win, text="Withdraw", command=withdraw, width=20).pack(pady=5)
    tk.Button(atm_win, text="Check Balance", command=check_balance, width=20).pack(pady=5)

# ================= MAIN BUTTONS =================
tk.Button(root, text="Add / Join Queue", command=add_user, width=25).pack(pady=5)
tk.Button(root, text="Serve Next User", command=serve_user, width=25).pack(pady=5)
tk.Button(root, text="Refresh Queue", command=update_queue, width=25).pack(pady=5)

root.mainloop()