feedbacks = [
    "The peer review highlighted strengths in your code structure and adherence to naming conventions, which enhance readability. ",
    "Areas for improvement include adding more comprehensive comments to critical sections and optimizing the database queries to reduce response times. ",
    "Great job maintaining test coverage; however, consider refining edge case scenarios. Overall, solid contribution with room for small refinements. Keep up the good work!",
]


def get_total_feedback_summary(user_id: int) -> str:
    # TODO: add real LLM interaction
    return feedbacks[user_id % len(feedbacks)]
