from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm
from extensions import db

from models import User, Problem, TestCase, Submission
from runner import execute_python
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import json
 
main = Blueprint("main", __name__)



@main.route("/")
def home():

    username = None

    if current_user.is_authenticated:
        username = current_user.username

    return render_template(
        "home.html",
        username=username
    )

@main.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        password_hash = generate_password_hash(
            form.password.data
        )

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful! You can now log in.",
            "success"
        )

        return redirect(
            url_for("main.login")
        )

    return render_template(
        "register.html",
        form=form
    )

@main.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password_hash,
            form.password.data
        ):

            login_user(user)

            return redirect(
                url_for("main.dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html",
        form=form
    )

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/problems")
def problems():
    problems = Problem.query.order_by(Problem.id).all()

    return render_template(
        "problems.html",
        problems=problems
    )

@main.route("/problems/<int:problem_id>")
def problem_detail(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    test_cases = TestCase.query.filter(
        TestCase.problem_id == problem.id,
        TestCase.is_hidden.is_(False)
    ).order_by(TestCase.id).all()

    print("PUBLIC TEST CASES:", test_cases)

    return render_template(
        "problem_detail.html",
        problem=problem,
        test_cases=test_cases
    )

@main.route("/problems/<int:problem_id>/submit", methods=["POST"])
@login_required
def submit_solution(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    code = request.form["code"]
    language = request.form["language"]

    submission = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        code=code,
        language=language,
        status="Pending"
    )

    db.session.add(submission)
    db.session.commit()

    test_cases = TestCase.query.filter_by(
        problem_id=problem.id
    ).order_by(TestCase.id).all()

    final_status = "Accepted"
    total_execution_time = 0

    passed_tests = 0
    total_tests = len(test_cases)

    test_results = []

    for test_case in test_cases:

        result = execute_python(
            code,
            input_data=json.dumps(test_case.input_data)
        )

        total_execution_time += result["execution_time"]

        # Runtime Error / TLE
        if result["status"] != "Success":

            final_status = result["status"]

            test_results.append({
                "test_case_id": test_case.id,
                "passed": False,
                "hidden": test_case.is_hidden
            })

            if test_case.is_hidden:
                submission.error_message = (
                    "A hidden test case failed."
                )
            elif result["status"] == "Runtime Error":
                submission.error_message = result["output"]
            elif result["status"] == "Time Limit Exceeded":
                submission.error_message = (
                    "Execution exceeded the 2 second time limit."
                )

            break

        actual_output = result["output"].strip()

        # Invalid JSON output
        try:
            actual_output = json.loads(actual_output)

        except json.JSONDecodeError:

            final_status = "Wrong Answer"

            test_results.append({
                "test_case_id": test_case.id,
                "passed": False,
                "hidden": test_case.is_hidden
            })

            if test_case.is_hidden:
                submission.error_message = (
                    "A hidden test case failed."
                )
            else:
                submission.error_message = (
                    "Your program did not produce valid JSON output."
                )

            break

        # Wrong Answer
        if actual_output != test_case.expected_output:

            final_status = "Wrong Answer"

            test_results.append({
                "test_case_id": test_case.id,
                "passed": False,
                "hidden": test_case.is_hidden
            })

            if test_case.is_hidden:
                submission.error_message = (
                    "A hidden test case failed."
                )
            else:
                submission.error_message = (
                    f"Expected: {test_case.expected_output}\n"
                    f"Got: {actual_output}"
                )

            break

        # Passed
        passed_tests += 1

        test_results.append({
            "test_case_id": test_case.id,
            "passed": True,
            "hidden": test_case.is_hidden
        })

    submission.status = final_status
    submission.execution_time = total_execution_time
    submission.passed_tests = passed_tests
    submission.total_tests = total_tests
    submission.test_results = test_results

    db.session.commit()

    return redirect(
        url_for(
            "main.submission_result",
            submission_id=submission.id
        )
    )

@main.route("/submissions/<int:submission_id>")
@login_required
def submission_result(submission_id):

    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user.id:
        return "Unauthorized", 403

    return render_template(
        "submission_result.html",
        submission=submission
    )

@main.route("/submissions")
@login_required
def submissions():

    submissions = Submission.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Submission.submitted_at.desc()
    ).all()

    return render_template(
        "submissions.html",
        submissions=submissions
    )


@main.route("/submissions/<int:submission_id>/detail")
@login_required
def submission_detail(submission_id):

    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user.id:
        return "Unauthorized", 403

    return render_template(
        "submission_detail.html",
        submission=submission
    )





@main.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        name = request.form["name"]
        return f"Hello {name}!"

    return render_template("hello.html")


@main.route("/about")
def about():
    return render_template("about.html")