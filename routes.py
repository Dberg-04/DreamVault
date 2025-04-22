from flask import render_template, redirect, url_for, request, session, flash

users = {"admin": "password"}
dreams = {}

def register_routes(app):
    @app.route("/")
    def home():
        if "user" in session:
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if username in users and users[username] == password:
                session["user"] = username
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid credentials")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("home"))

    @app.route("/dashboard")
    def dashboard():
        if "user" not in session:
            return redirect(url_for("login"))
        user_dreams = dreams.get(session["user"], [])
        return render_template("dashboard.html", dreams=user_dreams)

    @app.route("/add_dream", methods=["POST"])
    def add_dream():
        if "user" not in session:
            return redirect(url_for("login"))
        title = request.form["title"]
        content = request.form["content"]
        dreams.setdefault(session["user"], []).append((title, content))
        return redirect(url_for("dashboard"))
