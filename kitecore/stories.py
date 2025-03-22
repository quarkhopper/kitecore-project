# kitecore/stories.py

from lib.database import get_database
from lib.models import BaseMemory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

_db = get_database()
_engine = _db.get_engine()
_Session = sessionmaker(bind=_engine)

def add_story(name: str, story_text: str) -> int:
    """
    Adds a story with a unique name. Story must be 1000–2000 words.
    Raises ValueError if invalid or duplicate.
    """
    words = story_text.strip().split()
    if not (1000 <= len(words) <= 2000):
        raise ValueError("Story must be between 1000 and 2000 words.")

    session = _Session()
    try:
        story = BaseMemory(name=name, content=story_text)
        session.add(story)
        session.commit()
        return story.id
    except IntegrityError:
        session.rollback()
        raise ValueError(f"A story with name '{name}' already exists.")
    finally:
        session.close()


def list_stories() -> list[dict]:
    """
    Lists all stories by ID and name.
    """
    session = _Session()
    try:
        return [{"id": story.id, "name": story.name} for story in session.query(BaseMemory).all()]
    finally:
        session.close()
