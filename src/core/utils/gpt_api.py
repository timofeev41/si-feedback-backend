import os

from openai import OpenAI

feedbacks = [
    "The peer review highlighted strengths in your code structure and adherence to naming conventions, which enhance readability. ",
    "Areas for improvement include adding more comprehensive comments to critical sections and optimizing the database queries to reduce response times. ",
    "Great job maintaining test coverage; however, consider refining edge case scenarios. Overall, solid contribution with room for small refinements. Keep up the good work!",
]


class SyncLLMInterface:

    @staticmethod
    def _load_conn_args() -> dict:
        api_key = os.environ.get('LLM_API_KEY')
        assert api_key is not None, 'LLM_API_KEY must be specified'
        return dict(api_key=api_key)

    def __init__(self, model: str = 'gpt-4o-mini') -> None:
        self.client = OpenAI(**self._load_conn_args())
        self.model = model

    def perform_query(self, query: list[dict]):
        return self.client.chat.completions.create(
            messages=query,
            model=self.model
        )


def get_total_feedback_summary(user_id: int) -> str:
    # TODO: add real LLM interaction
    return feedbacks[user_id % len(feedbacks)]
