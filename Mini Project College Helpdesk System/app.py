from flask import Flask, render_template, request, redirect
import random
import sqlite3

app = Flask(__name__)
def create_database():
    conn = sqlite3.connect("complaints.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COMPLAINTS(
            complaint_id TEXT PRIMARY KEY,
            name TEXT,
            roll TEXT,
            catagory TEXT,
            location TEXT,
            description TEXT,
            status TEXT
            )
        """)
    
    conn.commit()
    conn.close()


create_database()

@app.route("/")
def home():
    return render_template("index.html")

#Reports
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        category = request.form["category"]
        location = request.form["location"]
        description = request.form["description"]

        complaint_id = "CC-" + str(random.randint(1000, 9999))

        conn= sqlite3.connect("complaints.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO complaints
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (complaint_id, name, roll, category, location, description, "Pending"))

        conn.commit()
        conn.close()

        return "Complaint recived! Your Complaint ID is:- " + complaint_id
    
    return render_template("report.html")

#Tracking of Complaints
@app.route("/track", methods=["GET", "POST"])
def track():

    if request.method == "POST":

        complaint_id = request.form["complaint_id"]
        conn = sqlite3.connect("complaints.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM complaints where complaint_id = ?",
            (complaint_id,)
        )

        complaint = cursor.fetchone()

        conn.close()

        if complaint:
            return "Complaint Found! Status: " + complaint[6]

        else:
            return "Complaint not Found."
    
    return render_template("track.html")

#Admin Login
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            return redirect("/admin/dashboard")

        else:
            return "Invalid username or password."

    return render_template("admin_login.html")

#Admin Dashboard
@app.route("/admin/dashboard")
def admin_dashboard():

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")

    complaints = cursor.fetchall()

    conn.close()

    return render_template("admin_dashboard.html", complaints=complaints)

#Update Button
@app.route("/admin/update_status", methods=["POST"])
def update_status():

    complaint_id = request.form["complaint_id"]
    status = request.form["status"]

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status = ? WHERE complaint_id = ?",
        (status, complaint_id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
