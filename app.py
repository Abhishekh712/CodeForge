from flask import Flask, render_template, request 
from extensions import db
from config import Config
from flask_migrate import Migrate
from models import User, Problem, Submission, TestCase
from routes import main
from flask_login import LoginManager
from admin_routes import admin

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(main)
app.register_blueprint(admin)



@app.route("/")
def home():
    username = "Abhishekh77"
    return render_template("home.html", username=username)

@app.route("/hello", methods=["GET", "POST"])
def hello():

    if request.method == "POST":
        name = request.form["name"]
        return f"Hello {name}!"

    return render_template("hello.html")

@app.route("/about")
def about():
    return render_template("about.html") 

@app.route("/db-test")
def db_test():
    db.session.execute(db.text("SELECT 1"))
    return "Database connection successful!"

if __name__ == "__main__":
    app.run(debug=True)