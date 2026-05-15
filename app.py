import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "tourmate_secret_key"
# Database initialization

def init_db():
    conn = sqlite3.connect('tourmate.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS tours
                 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    destination TEXT,
                    budget INTEGER,
                    date TEXT,
                    max_size INTEGER,
                    current_members INTEGER,
                    hotel TEXT,
                    transport TEXT,
                    description TEXT
                 )''')
    c.execute("SELECT COUNT(*) FROM tours")

    if c.fetchone()[0] == 0:
        dummy_tours = [
            ('সাজেক ভ্যালি এডভেঞ্চার', 'রাঙ্গামাটি', 4500, '2026-06-15', 10, 3, 'রিসোর্ট', 'চাঁদের গাড়ি', 'মেঘের রাজ্যে অপূর্ব এক ভ্রমণ।'),
            ('কক্সবাজার রিলাক্স ট্রিপ', 'কক্সবাজার', 6000, '2026-08-05', 8, 2, '৩ তারকা হোটেল', 'এসি বাস', 'সমুদ্রের পাড়ে সময় কাটান।')
        ]

        c.executemany(
            "INSERT INTO tours (name, destination, budget, date, max_size, current_members, hotel, transport, description) VALUES (?,?,?,?,?,?,?,?,?)",
            dummy_tours
        )

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tours')
def tours():
    conn = sqlite3.connect('tourmate.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tours ORDER BY id DESC")
    all_tours = c.fetchall()
    conn.close()

    return render_template('tours.html', tours=all_tours)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        budget = request.form['budget']
        date = request.form['date']
        max_size = request.form['max_size']
        hotel = request.form['hotel']
        description = request.form['description']

        conn = sqlite3.connect('tourmate.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO tours (name, destination, budget, date, max_size, current_members, hotel, transport, description) VALUES (?,?,?,?,?,?,?,?,?)",
            (name, destination, budget, date, max_size, 1, hotel, 'বাস', description)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('tours'))

    return render_template('create.html')


@app.route('/details/<int:id>')
def details(id):
    conn = sqlite3.connect('tourmate.db')
    c = conn.cursor()

    c.execute("SELECT * FROM tours WHERE id=?", (id,))
    tour = c.fetchone()

    conn.close()

    return render_template('details.html', tour=tour)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)