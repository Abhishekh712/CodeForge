from app import app
from extensions import db
from models import TestCase


test_cases = [
    TestCase(
        problem_id=1,
        input_data="[2,7,11,15], 9",
        expected_output="[0,1]"
    ),

    TestCase(
        problem_id=1,
        input_data="[3,2,4], 6",
        expected_output="[1,2]"
    ),

    TestCase(
        problem_id=2,
        input_data="[1,2,3,4,5], 4",
        expected_output="3"
    ),

    TestCase(
        problem_id=2,
        input_data="[1,3,5,7], 6",
        expected_output="-1"
    ),

    TestCase(
        problem_id=3,
        input_data="()[]{}",
        expected_output="True"
    ),

    TestCase(
        problem_id=3,
        input_data="([)]",
        expected_output="False"
    ),

    TestCase(
        problem_id=4,
        input_data="[[1,3],[2,6],[8,10],[9,12]]",
        expected_output="[[1,6],[8,12]]"
    )
]


with app.app_context():
    db.session.add_all(test_cases)
    db.session.commit()

    print("Test cases seeded successfully!")