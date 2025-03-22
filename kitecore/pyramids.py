# kitecore/pyramids.py

from typing import Optional, Dict, List
from kitecore import prompts
from lib.database import get_database
from lib.models import BaseMemory, MemoryPyramid, PyramidLevel
from sqlalchemy.orm import sessionmaker
import uuid

_db = get_database()
_engine = _db.get_engine()
_Session = sessionmaker(bind=_engine)


def extract_themes(story_id: int) -> list[str]:
    """
    Extracts up to 10 one-word themes from a story and stores them in the DB.
    Returns the list of extracted themes.
    """
    session = _Session()
    try:
        story = session.query(BaseMemory).filter_by(id=story_id).first()
        if not story:
            raise ValueError(f"Story with ID {story_id} not found.")

        prompt_text = prompts.render_prompt(
            prompts.EXTRACT_THEMES,
            {prompts.TAG_STORY: story.content}
        )

        # TODO: Call GPT with prompt_text and parse the comma-separated list
        response = "Calling, Discovery, Choice, Transformation, Sacrifice"  # Placeholder
        themes = [t.strip() for t in response.split(",") if t.strip()]

        # No DB storage needed unless one is selected for pyramid
        return themes
    finally:
        session.close()


def generate_pyramid(story_id: int, seed_theme: Optional[str] = None) -> Dict[str, str]:
    """
    Generates the pyramid by progressively compressing the story.
    Returns a dict of all levels: '1000', '500', '250', '100', '1-sentence'.
    """
    session = _Session()
    try:
        memory = session.query(BaseMemory).filter_by(id=story_id).first()
        if not memory:
            raise ValueError(f"Story with ID {story_id} not found.")

        pyramid = MemoryPyramid(base_id=story_id, theme=seed_theme)
        session.add(pyramid)
        session.commit()  # Commit so pyramid ID is assigned

        levels = {
            1: "1000",
            2: "500",
            3: "250",
            4: "100",
            5: "1-sentence",
        }

        results = {}
        current_text = memory.content

        for level, label in levels.items():
            if level < 5:
                prompt_name = prompts.CONDENSE_THEMATIC if seed_theme else prompts.CONDENSE
                replacements = {
                    prompts.TAG_WORDCOUNT: label,
                    prompts.TAG_STORY: current_text
                }
                if seed_theme:
                    replacements[prompts.TAG_THEME] = seed_theme
            else:
                prompt_name = prompts.ONE_SENTENCE_THEMATIC if seed_theme else prompts.ONE_SENTENCE
                replacements = {
                    prompts.TAG_STORY: current_text
                }
                if seed_theme:
                    replacements[prompts.TAG_THEME] = seed_theme

            prompt_text = prompts.render_prompt(prompt_name, replacements)

            # TODO: Call GPT with prompt_text and get result
            compressed_text = f"[Compressed to {label} words]"  # Placeholder
            results[label] = compressed_text

            session.add(PyramidLevel(
                pyramid_id=pyramid.id,
                level=level,
                content=compressed_text
            ))
            current_text = compressed_text

        session.commit()
        return results

    finally:
        session.close()


def get_pyramid_level(story_id: int, level: str) -> Optional[str]:
    """
    Fetches a single pyramid level for a story.
    Valid levels: '1000', '500', '250', '100', '1-sentence'
    """
    level_map = {
        "1000": 1,
        "500": 2,
        "250": 3,
        "100": 4,
        "1-sentence": 5
    }

    session = _Session()
    try:
        pyramid = session.query(MemoryPyramid).filter_by(base_id=story_id).first()
        if not pyramid:
            return None

        level_int = level_map.get(level)
        if level_int is None:
            raise ValueError(f"Invalid level '{level}'.")

        pl = session.query(PyramidLevel).filter_by(pyramid_id=pyramid.id, level=level_int).first()
        return pl.content if pl else None
    finally:
        session.close()

def get_pyramids() -> List[MemoryPyramid]:
    """
    Returns a list of all memory pyramids.
    """
    session = _Session()
    try:
        return session.query(MemoryPyramid).all()
    finally:
        session.close()


def delete_pyramid(pyramid_id: uuid.UUID) -> None:
    """
    Deletes a specific pyramid and its levels.
    """
    session = _Session()
    try:
        session.query(PyramidLevel).filter_by(pyramid_id=pyramid_id).delete()
        session.query(MemoryPyramid).filter_by(id=pyramid_id).delete()
        session.commit()
    finally:
        session.close()


def delete_all_pyramids() -> int:
    """
    Deletes all pyramids and associated levels.
    Returns the number of pyramids deleted.
    """
    pyramids = get_pyramids()
    for pyramid in pyramids:
        delete_pyramid(pyramid.id)
    return len(pyramids)

def delete_all_pyramids_for_story(story_name: str) -> int:
    """
    Deletes all pyramids related to a specific story by name.
    Returns the number of pyramids deleted.
    """
    session = _Session()
    try:
        # Get the story ID using the name
        story = session.query(BaseMemory).filter_by(name=story_name).first()
        if not story:
            print(f"[REST] Story with name '{story_name}' not found.")
            return 0
        
        # Delete pyramids related to this story
        pyramids = session.query(MemoryPyramid).filter_by(base_id=story.id).all()
        count = len(pyramids)
        
        for pyramid in pyramids:
            session.query(PyramidLevel).filter_by(pyramid_id=pyramid.id).delete()
            session.delete(pyramid)
        
        session.commit()
        print(f"[REST] {count} pyramid(s) related to '{story_name}' deleted.")
        return count
    finally:
        session.close()