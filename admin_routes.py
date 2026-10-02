from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models import User, Problem, Submission, TestCase
from flask_login import login_required, current_user
from functools import wraps
import json

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def admin_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if not current_user.is_admin:
            return "Forbidden", 403

        return func(*args, **kwargs)

    return wrapper




@admin.route("/")
@admin_required
def dashboard():

    total_users = User.query.count()

    total_problems = Problem.query.count()

    total_submissions = Submission.query.count()

    total_test_cases = TestCase.query.count()

    accepted_submissions = Submission.query.filter_by(
        status="Accepted"
    ).count()

    wrong_answers = Submission.query.filter_by(
        status="Wrong Answer"
    ).count()

    runtime_errors = Submission.query.filter_by(
        status="Runtime Error"
    ).count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_problems=total_problems,
        total_submissions=total_submissions,
        total_test_cases=total_test_cases,
        accepted_submissions=accepted_submissions,
        wrong_answers=wrong_answers,
        runtime_errors=runtime_errors
    )

@admin.route("/users")
@admin_required
def users():

    users = User.query.order_by(User.id).all()

    return render_template(
        "admin_users.html",
        users=users
    )

@admin.route("/users/<int:user_id>/make-admin", methods=["POST"])
@admin_required
def make_admin(user_id):

    user = User.query.get_or_404(user_id)

    user.is_admin = True

    db.session.commit()

    return redirect(url_for("admin.users"))

@admin.route("/users/<int:user_id>/remove-admin", methods=["POST"])
@admin_required
def remove_admin(user_id):

    user = User.query.get_or_404(user_id)

    user.is_admin = False

    db.session.commit()

    return redirect(url_for("admin.users"))


@admin.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent admin from deleting themselves
    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "error"
        )

        return redirect(url_for("admin.users"))

    # Delete the user's submissions first
    Submission.query.filter_by(
        user_id=user.id
    ).delete()

    username = user.username

    db.session.delete(user)
    db.session.commit()

    flash(
        f"User {username} deleted successfully.",
        "success"
    )

    return redirect(url_for("admin.users"))

@admin.route("/problems")
@admin_required
def problems():

    problems = Problem.query.order_by(
        Problem.id
    ).all()

    return render_template(
        "admin_problems.html",
        problems=problems
    )

@admin.route("/problems/create", methods=["GET", "POST"])
@admin_required
def create_problem():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        difficulty = request.form["difficulty"]
        category = request.form["category"]
        constraints = request.form["constraints"]

        problem = Problem(
            title=title,
            description=description,
            difficulty=difficulty,
            category=category,
            constraints=constraints
        )

        db.session.add(problem)
        db.session.commit()

        flash(
            f"Problem '{problem.title}' created successfully.",
            "success"
        )

        return redirect(
            url_for("admin.problems")
        )

    return render_template("admin_create_problem.html")

@admin.route("/problems/<int:problem_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_problem(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    if request.method == "POST":

        problem.title = request.form["title"]
        problem.description = request.form["description"]
        problem.difficulty = request.form["difficulty"]
        problem.category = request.form["category"]
        problem.constraints = request.form["constraints"]

        db.session.commit()

        flash(
            f"Problem '{problem.title}' updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.problems")
        )

    return render_template(
        "admin_edit_problem.html",
        problem=problem
    )

@admin.route("/problems/<int:problem_id>/delete", methods=["POST"])
@admin_required
def delete_problem(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    # Delete submissions belonging to this problem
    Submission.query.filter_by(
        problem_id=problem.id
    ).delete()

    # Delete test cases belonging to this problem
    TestCase.query.filter_by(
        problem_id=problem.id
    ).delete()

    problem_title = problem.title

    db.session.delete(problem)
    db.session.commit()

    flash(
        f"Problem '{problem_title}' deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.problems")
    )

@admin.route(
    "/problems/<int:problem_id>/test-cases",
    methods=["GET"]
)
@admin_required
def test_cases(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    test_cases = TestCase.query.filter_by(
        problem_id=problem.id
    ).order_by(
        TestCase.id
    ).all()

    return render_template(
        "admin_test_cases.html",
        problem=problem,
        test_cases=test_cases
    )

@admin.route(
    "/problems/<int:problem_id>/test-cases/create",
    methods=["POST"]
)
@admin_required
def create_test_case(problem_id):

    problem = Problem.query.get_or_404(problem_id)

    input_data = request.form["input_data"]
    expected_output = request.form["expected_output"]

    try:
        input_data = json.loads(input_data)
        expected_output = json.loads(expected_output)

    except json.JSONDecodeError:

        flash(
            "Input and expected output must be valid JSON.",
            "error"
        )

        return redirect(
            url_for(
                "admin.test_cases",
                problem_id=problem.id
            )
        )

    is_hidden = "is_hidden" in request.form

    test_case = TestCase(
        problem_id=problem.id,
        input_data=input_data,
        expected_output=expected_output,
        is_hidden=is_hidden
    )

    db.session.add(test_case)
    db.session.commit()

    flash(
        f"Test case added successfully to '{problem.title}'.",
        "success"
    )

    return redirect(
        url_for(
            "admin.test_cases",
            problem_id=problem.id
        )
    )

@admin.route(
    "/problems/<int:problem_id>/test-cases/<int:test_case_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def edit_test_case(problem_id, test_case_id):

    problem = Problem.query.get_or_404(problem_id)

    test_case = TestCase.query.filter_by(
        id=test_case_id,
        problem_id=problem.id
    ).first_or_404()

    if request.method == "POST":

        input_data = request.form["input_data"]
        expected_output = request.form["expected_output"]

        try:
            input_data = json.loads(input_data)
            expected_output = json.loads(expected_output)

        except json.JSONDecodeError:

            flash(
                "Input and expected output must be valid JSON.",
                "error"
            )

            return redirect(
                url_for(
                    "admin.edit_test_case",
                    problem_id=problem.id,
                    test_case_id=test_case.id
                )
            )

        test_case.input_data = input_data
        test_case.expected_output = expected_output
        test_case.is_hidden = "is_hidden" in request.form

        db.session.commit()

        flash(
            "Test case updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.test_cases",
                problem_id=problem.id
            )
        )

    return render_template(
        "admin_edit_test_case.html",
        problem=problem,
        test_case=test_case
    )

@admin.route(
    "/problems/<int:problem_id>/test-cases/<int:test_case_id>/delete",
    methods=["POST"]
)
@admin_required
def delete_test_case(problem_id, test_case_id):

    problem = Problem.query.get_or_404(problem_id)

    test_case = TestCase.query.filter_by(
        id=test_case_id,
        problem_id=problem.id
    ).first_or_404()

    db.session.delete(test_case)
    db.session.commit()

    flash(
        "Test case deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.test_cases",
            problem_id=problem.id
        )
    )

@admin.route("/submissions")
@admin_required
def submissions():

    submissions = Submission.query.order_by(
        Submission.submitted_at.desc()
    ).all()

    return render_template(
        "admin_submissions.html",
        submissions=submissions
    )

@admin.route("/submissions/<int:submission_id>")
@admin_required
def submission_detail(submission_id):

    submission = Submission.query.get_or_404(
        submission_id
    )

    return render_template(
        "admin_submission_detail.html",
        submission=submission
    )