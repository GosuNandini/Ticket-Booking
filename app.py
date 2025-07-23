from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                event TEXT,
                seats INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            if user:
                session["user_id"] = user[0]
                session["username"] = username
                return redirect("/book")
            else:
                return "Invalid credentials!"
    return render_template("login.html")


@app.route('/book', methods=["GET", "POST"])
def book():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        name = request.form["name"]
        event = request.form["event"]
        seats = request.form["seats"]
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO bookings (user_id, name, event, seats) VALUES (?, ?, ?, ?)",
                         (session["user_id"], name, event, seats))
        return redirect("/success")
    return render_template("book.html")


@app.route('/bookings')
def bookings():
    if "user_id" not in session:
        return redirect("/login")
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, event, seats FROM bookings WHERE user_id=?", (session["user_id"],))
        records = cur.fetchall()
    return render_template("bookings.html", records=records)

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    init_db()

    try:
        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("Nandini", "Nandini@04"))
        conn.commit()
        print("Admin user created.")
    except sqlite3.IntegrityError:
        print("Admin user already exists.")
    finally:
        conn.close()

    app.run(debug=True)




































# from flask import Flask, render_template, request, redirect, session, url_for
# import sqlite3

# app = Flask(__name__)
# app.secret_key = "secretkey"  # Needed for sessions

# def init_db():
#     with sqlite3.connect("database.db") as conn:
#         with open("schema.sql") as f:
#             conn.executescript(f.read())

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         with sqlite3.connect("database.db") as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
#             user = cur.fetchone()
#             if user:
#                 session["user_id"] = user[0]
#                 session["username"] = username
#                 return redirect("/book")
#             else:
#                 return "Invalid credentials!"
#     return render_template("login.html")

# @app.route('/book', methods=["GET", "POST"])
# def book():
#     if "user_id" not in session:
#         return redirect("/login")

#     if request.method == "POST":
#         name = request.form["name"]
#         event = request.form["event"]
#         seats = request.form["seats"]
#         with sqlite3.connect("database.db") as conn:
#             conn.execute("INSERT INTO tickets (user_id, name, event, seats) VALUES (?, ?, ?, ?)",
#                          (session["user_id"], name, event, seats))
#         return redirect("/success")
#     return render_template("book.html")

# @app.route('/bookings')
# def bookings():
#     if "user_id" not in session:
#         return redirect("/login")
#     with sqlite3.connect("database.db") as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT name, event, seats FROM tickets WHERE user_id=?", (session["user_id"],))
#         tickets = cur.fetchall()
#     return render_template("bookings.html", tickets=tickets)

# @app.route('/success')
# def success():
#     return render_template("success.html")

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect("/")

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)
# if __name__ == '__main__':
#     init_db()
    
#     conn = sqlite3.connect("database.db")
#     conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
#     conn.commit()
#     conn.close()

#     app.run(debug=True)
