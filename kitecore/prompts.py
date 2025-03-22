# kitecore/prompts.py

from lib.database import get_database
from lib.models import PromptTemplate
from sqlalchemy.orm import sessionmaker

# Prompt name constants
CONDENSE = "condense"
CONDENSE_THEMATIC = "condense_thematic"
ONE_SENTENCE = "one_sentence"
ONE_SENTENCE_THEMATIC = "one_sentence_thematic"
EXTRACT_THEMES = "extract_themes"

# Template tag constants
TAG_WORDCOUNT = "WORDCOUNT"
TAG_STORY = "STORY"
TAG_THEME = "THEME"

# Set up DB session
_db = get_database()
_engine = _db.get_engine()
_Session = sessionmaker(bind=_engine)

def get_prompt_template(name: str) -> str:
    """
    Fetches a prompt template string from the database by its name.
    """
    session = _Session()
    try:
        prompt_obj = session.query(PromptTemplate).filter_by(name=name).first()
        if not prompt_obj:
            raise ValueError(f"Prompt '{name}' not found in database.")
        return prompt_obj.template
    finally:
        session.close()

def fill_template(template: str, values: dict) -> str:
    """
    Replaces placeholders like [WORDCOUNT], [STORY], etc. with corresponding values.
    """
    for key, val in values.items():
        placeholder = f"[{key.upper()}]"
        template = template.replace(placeholder, val)
    return template

def render_prompt(name: str, values: dict) -> str:
    """
    Fetches a prompt by name and fills in the template with the given values.
    """
    template = get_prompt_template(name)
    return fill_template(template, values)
