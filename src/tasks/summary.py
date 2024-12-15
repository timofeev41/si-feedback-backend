import uuid
from datetime import datetime

import dramatiq

from src.core.utils.gpt_api import SyncLLMInterface
from loguru import logger


@dramatiq.actor
def summarize_feedback(feedback_data: dict, session_id: uuid.UUID) -> str | None:
    ts_now = datetime.now().isoformat()
    logger.info(f'Summarizing feedback for {session_id=}, {ts_now=}')
    llm = SyncLLMInterface()
    content = (f'Read this JSON {feedback_data}, '
               f'where key is a question about person '
               f'and value is how this person is rated by his colleague. '
               f'This is all related to employee performance testing session. '
               f'Summarize it in a few sentences and just send me your summary without any comments')
    query = [{'role': 'user', 'content': content}]
    try:
        return llm.perform_query(query).choices[0].message.content
    except Exception as e:
        logger.error(f'Failed to evaluate feedback - {e}')
        return None


@dramatiq.actor
def summarize_session(feedbacks_data: list[str], session_id: str) -> str | None:
    ts_now = datetime.now().isoformat()
    logger.info(f'Summarizing overall feedback for {session_id=}, {ts_now=}')
    llm = SyncLLMInterface()
    content = (f'Read this list of strings {feedbacks_data}, '
               f'where the values related to '
               f'employee performance testing session. Ignore None values.'
               f'Summarize them in a few sentences and just send me your overall summary about this person without any comments')
    query = [{'role': 'user', 'content': content}]
    try:
        return llm.perform_query(query).choices[0].message.content
    except Exception as e:
        logger.error(f'Failed to evaluate session overall feedback - {e}')
        return None

