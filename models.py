from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
    db.Boolean,
    nullable=False,
    default=False,
    server_default=db.text("false")
    )

class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    constraints = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    problem_id = db.Column(
        db.Integer,
        db.ForeignKey("problems.id"),
        nullable=False
    )

    code = db.Column(
        db.Text,
        nullable=False
    )

    language = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    execution_time = db.Column(
        db.Float
    )

    passed_tests = db.Column(
        db.Integer
    )

    total_tests = db.Column(
        db.Integer
    )

    error_message = db.Column(
        db.Text
    )

    test_results = db.Column(
        db.JSON
    )

    submitted_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship("User", backref="submissions")
    problem = db.relationship("Problem", backref="submissions")

class TestCase(db.Model):
    __tablename__ = "test_cases"

    id = db.Column(db.Integer, primary_key=True)

    problem_id = db.Column(
        db.Integer,
        db.ForeignKey("problems.id"),
        nullable=False
    )

    input_data = db.Column(
        db.JSON,
        nullable=False
    )

    expected_output = db.Column(
        db.JSON,
        nullable=False
    )

    problem = db.relationship(
        "Problem",
        backref="test_cases"
    )

    is_hidden = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.text("false")
    )