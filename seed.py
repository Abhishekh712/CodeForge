from app import app
from extensions import db
from models import Problem


problems = [
    Problem(
        title="Two Sum",
        description="Given an array of integers and a target, return the indices of the two numbers that add up to the target.",
        difficulty="Easy",
        category="Arrays",
        constraints="2 <= nums.length <= 10^4"
    ),

    Problem(
        title="Binary Search",
        description="Given a sorted array of integers, find the position of a target value using binary search.",
        difficulty="Easy",
        category="Binary Search",
        constraints="The array is sorted in ascending order."
    ),

    Problem(
        title="Valid Parentheses",
        description="Given a string containing brackets, determine whether the brackets are correctly matched and nested.",
        difficulty="Easy",
        category="Stack",
        constraints="The string contains only (), {}, and []."
    ),

    Problem(
        title="Merge Intervals",
        description="Given a collection of intervals, merge all overlapping intervals.",
        difficulty="Medium",
        category="Intervals",
        constraints="1 <= intervals.length <= 10^4"
    )
]


with app.app_context():
    db.session.add_all(problems)
    db.session.commit()

    print("Problems seeded successfully!")